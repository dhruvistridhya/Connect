from django.urls import path
from . import views 
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('login', views.LoginView.as_view(),name="login"),
    path('logout', auth_views.LogoutView.as_view(template_name='login.html'), name='logout'),
    path('register', views.RegistrationView.as_view(),name="register"),
    path('profile/',views.UserProfile.as_view(),name='profile'),
    # path('profile/<int:pk>',views.UserProfile.as_view(),name="profile_edit"),
    path('home',views.home,name='home'),
    path('users',views.getAllUser,name='users'),
    path('account',views.account,name='account'),


    path('getProfile',views.getProfile,name='profiles'),
    path('addProfile',views.addProfile,name='addprofile'),

    path('chatView',views.chatRoom,name="chat")
]