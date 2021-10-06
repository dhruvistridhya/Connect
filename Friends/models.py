from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

class FriendList(models.Model):

	user = models.ForeignKey(User,on_delete=models.CASCADE, related_name='user')
	friends = models.ManyToManyField(User, related_name="friends", blank=True)

	def __str__(self):
		return self.user.username

	def add_friend(self,account):

		if not account in self.friends.all():
			self.friends.add(account)
			self.save()

	def remove_friend(self,account):

		if account in self.friends.all():
			self.friends.delete(account)
			print("*"*100)
			self.save()

	def unfriend(self,removee):

		remover_friends_list = self

		#Remove friend from friendlist
		remover_friends_list.remove_friend(removee)

		#Removing user from removee's friendlist
		friend_list = FriendList.objects.get(user=removee)
		friend_list.remove_friend(self.user)

	def is_mutual_friend(self,friend):
		if friend in self.friends:
			return True
		return False


class FriendRequest(models.Model):

	sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender")
	receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="receiver")
	is_active = models.BooleanField(blank=True, null=False, default=True)
	timestamp = models.DateTimeField(auto_now_add= True)

	def __str__(self):
		return self.sender.username

	def accept(self):

		receiver_friend_list = FriendList.objects.get(user=self.receiver)
		if receiver_friend_list:
			receiver_friend_list.add_friend(self.sender)
			sender_friend_list = FriendList.objects.get(user=self.sender)
			if sender_friend_list:
				sender_friend_list.add_friend(self.receiver)
				self.is_active=False
				self.save()

	# receiver canceling the request
	def decline(self):
		self.is_active=False
		self.save()

	# sender canceling the request
	def cancel(self):
		self.is_active=False
		self.save()