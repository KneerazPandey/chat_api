import uuid
from django.db import models
from core.events.registry import EventRegistry
from apps.chats.events import MessageSentEvent
from apps.chats.models import Message, Room


@EventRegistry.register('chats.message.sent.event', is_async_task=True)
def save_message_handler(event: MessageSentEvent):
    Message.objects.create(
        id=uuid.UUID(event.message_id) if isinstance(event.message_id, str) else event.message_id,
        sender_id=uuid.UUID(event.sender_id) if isinstance(event.sender_id, str) else event.sender_id,
        room_id=uuid.UUID(event.room_id) if isinstance(event.room_id, str) else event.room_id,
        text=event.text,
    )
    Room.objects.filter(id=event.room_id).update(updated_at=models.functions.Now())