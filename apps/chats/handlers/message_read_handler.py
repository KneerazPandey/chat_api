from core.events.registry import EventRegistry
from apps.chats.events import MessageReadReceiptEvent
from apps.chats.tasks import mark_message_as_read_in_db
from channels.layers import get_channel_layer



@EventRegistry.register('chats.message.read.receipt.event', is_async=False)
async def message_read_handler(event: MessageReadReceiptEvent):
    channel_layer = get_channel_layer()
    group_name = f"chat_{event.room_id}"
    
    # Broadcast to other users that this specific message was read
    await channel_layer.group_send(
        group_name,
        {
            "type": "chat.message.read",
            "message_id": str(event.message_id),
            "reader_id": str(event.user_id)
        }
    )

    # 2. BACKGROUND DATABASE WRITE: Offload the heavy SQL operation to Celery!
    # This runs asynchronously without blocking Uvicorn's event loop.
    mark_message_as_read_in_db.delay(
        message_id=str(event.message_id), 
        user_id=str(event.user_id)
    )