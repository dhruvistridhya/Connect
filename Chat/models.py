from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Room(models.Model):

	title = models.CharField(max_length=10,primary_key=True)
	user1 = models.ForeignKey(User, related_name='user1', on_delete = models.CASCADE)
	user2 = models.ForeignKey(User, related_name='user2', on_delete = models.CASCADE)


class Message(models.Model):

	author = models.ForeignKey(User, related_name='author_messages',on_delete = models.CASCADE)
	content = models.TextField()
	timestamp = models.DateTimeField(auto_now_add=True)
	room = models.ForeignKey(Room, related_name='room', on_delete=models.CASCADE)

	def __str__(self):
		return self.author.username

	def last_10_messages(room):
		return Message.objects.order_by('-timestamp').all()[:10]