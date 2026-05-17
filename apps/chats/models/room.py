import uuid
from django.db import models


class Room(models.Model):
    """Represents a chat room. Can be 1-to-1 or a Group."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, blank=True, null=True)  # Null for 1-to-1 chats
    is_group = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  # Crucial for sorting chat lists

    class Meta:
        indexes = [
            models.Index(fields=['-updated_at']) # Fast fetching of user's recent chats
        ]

    def __str__(self):
        return self.name or f"Private Chat {self.id}"