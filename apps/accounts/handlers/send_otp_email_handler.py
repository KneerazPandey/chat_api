from apps.accounts.events import UserRegisteredOtpRequestedEvent
from core.events.registry import EventRegistry
from apps.accounts.tasks import send_user_registered_otp_task


@EventRegistry.register('accounts.user.registered.otp.requested.event')
def send_otp_email_handler(event: UserRegisteredOtpRequestedEvent):
    send_user_registered_otp_task.delay(
        email=event.email,
        otp=event.otp
    )