from uuid import UUID
from dataclasses import dataclass, field
from core.events import BaseEvent


@dataclass(frozen=True, kw_only=True)
class MessageSentEvent(BaseEvent):
    message_id: str | UUID
    room_id: str | UUID
    sender_id: str | UUID
    text: str 

    event_name: str = field(default='chats.message.sent.event', init=False)