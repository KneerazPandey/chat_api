from dataclasses import dataclass, field
from core.events import BaseEvent


@dataclass(frozen=True, kw_only=True)
class MessageReadReceiptEvent(BaseEvent):
    room_id: str
    user_id: str
    message_id: str
    
    event_name: str = field(default='chats.message.read.receipt.event', init=False)