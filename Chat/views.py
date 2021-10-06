from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.safestring import mark_safe
import json
from .models import Room
from django.shortcuts import redirect
from django.db.models import Q

# Create your views here.
def index(request):
	return render(request, 'chat/index.html')

@login_required
def room(request, room_name):
	print(request.user.username)
	return render(request, 'chat/room.html',{
		'room_name': mark_safe(json.dumps(room_name)),
		'username': mark_safe(json.dumps(request.user.username))
	})

def getChatRoom(request,id):
	user1 = request.user.id
	room_name = Room.objects.filter( Q(user1=user1,user2=id) | Q(user1=id,user2=user1)).values_list('title',flat=True).first()
	print(room_name)
	url=room_name+'/'
	return redirect(url)

def mainChat(request):
	context={}
	return render(request,'chat/chatMain.html',context=context)