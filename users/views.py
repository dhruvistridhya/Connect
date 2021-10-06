from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login, logout
from django.contrib.auth.hashers import make_password

from .serializers import LoginSerializer, RegistrationSerializer, ProfileSerializer, UserSerializer
from .models import Profile

from django.contrib import messages

from django.http import HttpResponseRedirect, HttpResponse

from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response

from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view,renderer_classes
from rest_framework.views import APIView
from django.shortcuts import redirect

from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
# Create your views here.


class LoginView(APIView):

	renderer_classes = [TemplateHTMLRenderer]
	template_name = 'login.html'

	def post(self,request):
		s1 = LoginSerializer(data=request.data)
		print(s1)
		s1.is_valid(raise_exception=True)
		user = s1.validated_data["user"]
		login(request,user)

		session_user = User.objects.filter(username=self.request.data['username']).first()
		# print(session_user.id)

		token, created = Token.objects.get_or_create(user=user)
		request.session['user_token']=token.key
		request.session['user']=session_user.id

		print(request.session['user_token'])
		profile = Profile.objects.all()
		print(profile)
		# return Response({"token":token.key,"msg":"login Successfully"},status=200)
		# return render(request,'home.html',{"profile":profile})
		return redirect('home')

	def get(self,request):
		return Response({"msg":"worked"})


class RegistrationView(APIView):

	renderer_classes = [TemplateHTMLRenderer]
	template_name = 'login.html'

	def post(self,request):
		print("#"*100)
		username = self.request.data['username']
		email =  self.request.data['email']
		password = self.request.data['password']
		password2 = self.request.data['password2']
		print(username)
		if password == password2:
			data={
				"username":username,
				"email":email,
				"password":make_password(password)
			}
			print(data['password'])
			s1 = RegistrationSerializer(data=data)
			print("*"*100)
			if s1.is_valid():
				print("*"*100)
				s1.save()
				# return Response(s1.data,status=status.HTTP_201_CREATED)
				return redirect('login')
			return Response(s1.errors, status=status.HTTP_400_BAD_REQUEST)
		else:
			messages.success(request,"Enter same password in both field")
			return Response({"msg":"Enter same password in both field"}, status=status.HTTP_400_BAD_REQUEST)

	def get(self,request):
		return Response({"msg":"worked"})

@login_required
def home(request):
	print(request.user)
	profile = Profile.objects.all().exclude(user=request.user.id)
	print(profile)
	return render(request,'chat/chatRoom.html',{"profile":profile})

@api_view(('GET',))
def getAllUser(APIView):
	users = User.objects.all()
	u1 = UserSerializer(users,many=True)
	return Response(u1.data,status=302)

class UserProfile(APIView):

	def post(self,request):
		print("*"*100)
		# uid = request.session['user']
		s1 = ProfileSerializer(data = request.data)
		if s1.is_valid():
			s1.save()
			return Response({"msg":"working"})
		return Response({"msg":"not working"})

	def put(self,request,pk):
		try:
			profile = Profile.objects.get(pk=pk)
		except Profile.DoesNotExist:
			return HttpResponse(status=404)

		s1 = ProfileSerializer(profile,data=request.data)
		# print(s1)
		if s1.is_valid():		
			s1.save()
			return Response({"msg":"Working"})
		return Response({"msg":"Not Working"})

	def get(self,request):
		profiles = Profile.objects.all()
		ps = ProfileSerializer(profiles,many=True)
		return Response(ps.data,status=302)

def account(request):
	return render(request,'account.html')


# def add(request):
# 	return Response({"msg":"FO"})

@api_view(('GET',))
@login_required
def getProfile(request):
	print("*"*100)
	print(request.user)
	profiles = Profile.objects.all()
	s1 = ProfileSerializer(profiles,many=True)
	return Response(s1.data,status=302)

@api_view(('GET','POST'))
@login_required
def addProfile(request):
	print(request.user)
	if request.method=='POST':
		s1 = ProfileSerializer(data = request.data)
		if s1.is_valid():
			s1.save()
			return Response({"msg":"working"})
		return Response({"msg":"not working"})

def chatRoom(request):
	return render(request,"chat.html")