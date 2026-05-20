import uuid
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from apps.chats.selectors import RoomMemberSelector
from apps.chats.events import MessageSentEvent
from core.events.dispatcher import EventDispatcher



class ChatConsumer(AsyncJsonWebsocketConsumer):
    async def accept(self, subprotocol = None, headers = None):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'chat_{self.room_id}'
        self.user = self.scope['user']

        # 1. Security Check: Reject unauthenticated users
        if self.user.is_anonymous:
            await self.close(code=4001)
            return 
        
        # 2. Security Check: Ensure user is actually a member of this conversation
        is_member = await RoomMemberSelector.check_membership(
            user=self.user,
            room_id=self.room_id
        )
        if not is_member:
            await self.close(code=4003)
            return 
        
        # Join the conversation group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        return await super().accept(subprotocol, headers)
    
    async def disconnect(self, code):
        # Leave the conversation group
        if hasattr(self, 'room_group_name'):
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )
            
        return await super().disconnect(code)
    
    async def receive_json(self, content, **kwargs):
        print('---Data Received in json by consumer------')
        message_text = content.get('text', '').strip()
        print(message_text)

        # Guard clause: Don't process empty messages
        if not message_text:
            return
        
        # 1. Initializing Event Data
        message_id = str(uuid.uuid4())
        event = MessageSentEvent(
            message_id=message_id,
            room_id=self.room_id,
            sender_id=self.user.id,
            text=message_text,
        )
        await EventDispatcher.dispatch(event=event)
        print('Event Dispatched Successfully')
    
    async def send_chat(self, event):
        await self.send_json(event['data'])