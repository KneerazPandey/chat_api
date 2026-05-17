import uuid
from django.db import models
from django.contrib.auth import get_user_model
from .room import Room


User = get_user_model()


class RoomMember(models.Model):
    """Through table tracking who is in which room."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="members")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="rooms")
    joined_at = models.DateTimeField(auto_now_add=True)
   
    last_read_message_id = models.UUIDField(blank=True, null=True)  # Track the last message read by this specific user for unread badge counts

    class Meta:
        unique_together = ('room', 'user')
        indexes = [
            models.Index(fields=['user', 'room'])
        ]