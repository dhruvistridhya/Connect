from django.urls import path

from . import views

urlpatterns = [
    path('chat/', views.index, name='index'),
    path('chat/<str:room_name>/', views.room, name='room'),
    path('chat/<int:id>',views.getChatRoom,name='chatRoomName'),
    path('mainChat',views.mainChat,name='main')
]