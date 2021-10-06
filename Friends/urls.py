from django.urls import path
from . import views 

urlpatterns = [
    path('addFriendList', views.postFriendList,name="addFriendList"),
    path('addFriend/<int:pk>',views.addFriendView,name="addFriend"),
    path('removeFriend/<int:pk>',views.removeFriendView,name="removeFriend"),
]