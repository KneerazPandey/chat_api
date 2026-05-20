import uuid
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from apps.chats.selectors import RoomMemberSelector
from apps.chats.events import MessageSentEvent, UserTypingEvent, MessageReadReceiptEvent
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
        event_type = content.get("type")
        message_text = content.get('text', '').strip()

        # 1. Handle Typing Status
        if event_type == "typing":
            event = UserTypingEvent(
                room_id=self.room_id,
                user_id=self.scope["user"].id,
                username=self.scope["user"].username,
                is_typing=content.get("is_typing", False)
            )
            await EventDispatcher.dispatch_async(event)
            return
        
        # 2. Handle Read Receipts
        elif event_type == "read_receipt":
            event = MessageReadReceiptEvent(
                room_id=self.room_id,
                user_id=self.scope["user"].id,
                message_id=content.get("message_id")
            )
            await EventDispatcher.dispatch_async(event)
            return
        
        # 3. Fallback to your existing MessageSentEvent logic
        elif event_type == "message":
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
    
    async def send_chat(self, event):
        await self.send_json(event['data'])

    async def chat_typing_status(self, event):
        """Triggered when user_typing_handler calls group_send"""
        # Don't echo the typing indicator back to the person who is typing!
        if event["user_id"] != str(self.scope["user"].id):
            await self.send_json(event)

    async def chat_message_read(self, event):
        """Triggered when message_read_handler calls group_send"""
        await self.send_json(event)