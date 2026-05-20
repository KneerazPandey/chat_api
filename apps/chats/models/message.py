import uuid
from django.db import models
from .room import Room
from django.contrib.auth import get_user_model


User = get_user_model()


class Message(models.Model):
    """
    Stores the individual text/media payloads.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="sent_messages")
    text = models.TextField(blank=True, null=True)
    media_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']  # Default to latest first
        indexes = [
            # Compound index for loading page-by-page history inside a specific chat
            models.Index(fields=['room', '-created_at']), 
        ]

    def __str__(self):
        return f"{self.sender} in {self.id}: {self.text[:20]}"