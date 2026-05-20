from dataclasses import dataclass, field
from core.events import BaseEvent

@dataclass(frozen=True, kw_only=True)
class UserTypingEvent(BaseEvent):
    room_id: str
    user_id: str
    username: str
    is_typing: bool  # True when typing, False when stopped
    
    event_name: str = field(default='chats.user.typing.event', init=False)