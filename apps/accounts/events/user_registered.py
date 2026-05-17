from dataclasses import dataclass

from core.events.base import BaseEvent


@dataclass(frozen=True, kw_only=True)
class UserRegisteredOtpRequestedEvent(BaseEvent):

    email: str
    otp: str

    event_name: str = "accounts.user.registered.otp.requested.event"