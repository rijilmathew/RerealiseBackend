# views.py

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from .models import Room, Message
from .serializers import RoomSerializer, MessageSerializer,UnseenMessagesCountSerializer,MessageCountSerializer
from django.shortcuts import get_object_or_404
from authentification.models import User
from django.http import JsonResponse

class CreateRoomView(CreateAPIView):
    serializer_class = RoomSerializer

    def create(self, request, *args, **kwargs):
        care_home_id = request.data.get('care_home_id')
        user_id = request.data.get('user_id')
        provider_id = request.data.get('provider_id')
        username=request.data.get('username')
        print(username)

        # Construct a more unique room name using both care_home_id and user_id
        room_name = f"CareHome_{provider_id}_{user_id}"

        # Check if the room already exists
        existing_room = Room.objects.filter(name=room_name).first()
        if existing_room:
            print('alredy have ')
            return Response(RoomSerializer(existing_room).data, status=status.HTTP_200_OK)
        
        try:
            provider = User.objects.get(id=provider_id)
        except User.DoesNotExist:
            return Response({"error": "Provider not found."}, status=status.HTTP_400_BAD_REQUEST)


        # Create room
        room = Room(name=room_name,provider=provider,username=username)
        room.save()

        serializer = RoomSerializer(room)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class MessageList(generics.ListCreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer


class Last50MessagesView(generics.ListAPIView):
    serializer_class = MessageSerializer

    def get_queryset(self):
        room_name = self.kwargs['room_name']
        room = get_object_or_404(Room, name=room_name)
        return Message.objects.filter(room=room).order_by('timestamp')[:50]


class ProviderChatRoomsView(generics.ListAPIView):
    serializer_class = RoomSerializer

    def get_queryset(self):
        provider_id = self.kwargs['provider_id']
        return Room.objects.filter(provider__id=provider_id)
    

class UnseenMessagesCountView(APIView):
    @staticmethod
    def get(request, room_id):
        room = get_object_or_404(Room, id=room_id)
        unseen_count = room.messages.filter(is_seen=False).count()

        serializer = UnseenMessagesCountSerializer({'unseen_count': unseen_count})
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class MarkMessagesAsSeenView(generics.UpdateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def update(self, request, *args, **kwargs):
        room_id = kwargs.get('room_id')
        room = get_object_or_404(Room, id=room_id)
        messages = room.messages.filter(is_seen=False)
        
        # Mark messages as seen
        messages.update(is_seen=True)

        return Response({'success': True})
    

class TotalMessageCountView(generics.ListAPIView):
    serializer_class = MessageCountSerializer

    def get_queryset(self):
        provider_id = self.kwargs['provider_id']
        rooms = Room.objects.filter(provider__id=provider_id)
        total_message_count = Message.objects.filter(room__in=rooms,is_seen=False).count()

        return [{'provider_id': provider_id, 'total_message_count': total_message_count}]