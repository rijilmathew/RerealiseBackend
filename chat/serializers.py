# serializers.py

from rest_framework import serializers
from .models import Message, Room

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields ='__all__'

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'user', 'content', 'timestamp','is_seen']

    # # You can include serializers for the sender and receiver fields if needed
    # sender = serializers.StringRelatedField()
    # receiver = serializers.StringRelatedField()

class UnseenMessagesCountSerializer(serializers.Serializer):
    unseen_count = serializers.IntegerField()

class MessageCountSerializer(serializers.Serializer):
    provider_id = serializers.IntegerField()
    total_message_count = serializers.IntegerField()
