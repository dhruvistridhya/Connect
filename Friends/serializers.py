from rest_framework import serializers

from .models import FriendList

class FriendListSerializer(serializers.ModelSerializer):

	class Meta:
		model = FriendList
		fields = '__all__'