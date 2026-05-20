from core.events.registry import EventRegistry
from channels.layers import get_channel_layer
from apps.chats.events import UserTypingEvent


@EventRegistry.register('chats.user.typing.event', is_async=False)
async def user_typing_handler(event: UserTypingEvent):
    channel_layers = get_channel_layer()
    group_name = f"chat_{event.room_id}"

    await channel_layers.group_send(
        group_name,
        {
            "type": "chat.typing.status", 
            "user_id": str(event.user_id),
            "username": event.username,
            "is_typing": event.is_typing
        }
    )