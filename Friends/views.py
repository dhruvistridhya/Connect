from django.shortcuts import render
from .models import FriendList
from .serializers import FriendListSerializer

from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect, HttpResponse

from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer

# Create your views here.

def postFriendList(request):
	print(request.user.id)
	data = {
		"user":request.user.id
	}
	s1 = FriendListSerializer(data=data)
	print(s1)
	if s1.is_valid():
		s1.save()
		return HttpResponse({"working"})
	return HttpResponse("Not Working")

@login_required
def addFriendView(request,pk):
	# print(request.user)
	u1 = FriendList.objects.filter(user=request.user.id).first()
	# print(u1)
	u1.add_friend(pk)
	# s1 = FriendList.objects.all()
	# print(s1)
	return HttpResponse("working")

@login_required
def removeFriendView(request,pk):
	print(request.user)
	u1 = FriendList.objects.filter(user=request.user.id).first()
	u1.friends.remove(pk)
	return HttpResponse("Working")