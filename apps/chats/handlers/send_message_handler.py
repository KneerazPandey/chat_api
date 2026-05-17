from apps.chats.events import MessageSentEvent
from core.events.registry import EventRegistry
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


@EventRegistry.register('chats.message.sent.event', is_async_task=False)
def send_message_handler(event: MessageSentEvent):
    """Broadcasts the message over WebSockets instantly."""
    channel_layer = get_channel_layer()
    room_group_name = f'chat_{event.room_id}'

    async_to_sync(channel_layer.group_send(
        room_group_name,
        {
            'type': 'send_chat',  # Triggers the send_chat method in consumer
            'data': {
                'id': event.message_id,
                'room_id': event.room_id,
                'sender_id': event.sender_id,
                'text': event.text,
                'created_at': event.created_at 
            }
        }
    ))