from django.db import models
from authentification.models import User


class Room(models.Model):
    name = models.CharField(max_length=255, unique=True)
    provider= models.ForeignKey(User, on_delete=models.CASCADE, related_name='provider_room')
    username= models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='messages')
    is_seen = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.User.username} to {self.room.name}"
