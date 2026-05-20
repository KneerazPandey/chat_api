from core.events.registry import EventRegistry
from channels.layers import get_channel_layer


@EventRegistry.register('chats.message.sent.event', is_async_task=False)
async def send_message_handler(event):
    print('Message sending using websocket')
    """Broadcasts the message over WebSockets instantly."""
    channel_layer = get_channel_layer()
    room_group_name = f'chat_{event.room_id}'

    await channel_layer.group_send(
        room_group_name,
        {
            'type': 'send_chat',  # Triggers the send_chat method in consumer
            'data': {
                'id': str(event.message_id),
                'room_id': str(event.room_id),
                'sender_id': str(event.sender_id),
                'text': event.text
            }
        }
    )