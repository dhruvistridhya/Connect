import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from .models import Message,Room
from django.contrib.auth.models import User
 
class ChatConsumer(WebsocketConsumer):

    def calling_method(self,data):
        message = data['message']
        print(message)
        # data['message']['receiver_channel_name'] = self.channel_name

        self.send(text_data=json.dumps(data))

    def fetch_messages(self,data):
        print(data)
        print(self.room_name)
        messages = Message.last_10_messages(self.room_name) 
        content = {
            'command':'messages',
            'messages' : self.messages_to_json(messages)
        }
        self.send_message(content)

    def new_message(self,data):
        author = data['from']
        author_user = User.objects.filter(username=author)[0]
        room = Room.objects.filter(title=data['room']).first()
        message = Message.objects.create(author = author_user, content = data['message'], room=room)
        content = {
            'command':'new_message',
            'message':self.message_to_json(message)
        }
        return self.send_chat_message(content)

    def messages_to_json(self,messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        return result

    def message_to_json(self,message):
        return{
            'author': message.author.username,
            'content':message.content,
            'timestamp': str(message.timestamp)
        }

    command = {
        'fetch_messages': fetch_messages,
        'new_message': new_message,
        'new-peer':calling_method
    }

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        data = json.loads(text_data)
        print(data,"receive signal")
        self.command[data['command']](self,data)

    def send_chat_message(self,message):
        # message = data['message']
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    def send_message(self,message):
        self.send(text_data=json.dumps(message))

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps(message))

class VideoChatConsumer(WebsocketConsumer):
    
    async def connect(self):
        self.room_group_name='Test-Room'

        await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
        )

        print('disconnected!')

    async def receive(self, dict_data):
        receive_dict = json.loads(dict_data)
        message = receive_dict['message']

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type':'send.message',
                'message': message
            }
        )

    async def send_message(self,event):
        message = event['message']

        await self.send(text_data=json.dumps({
                'message':message
        }))