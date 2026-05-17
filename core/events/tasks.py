from celery import shared_task
from django.utils.module_loading import import_string

@shared_task(
    bind=True,
    max_retries=3,
    default_retry_delay=2,
    ack_late=True
)
def execute_event_handler_async(self, handler_path: str, event_path: str, event_data: dict):
    try:
        # 1. Dynamically import the handler function (e.g., save_message_handler)
        handler = import_string(handler_path)

        # 2. Dynamically import the event class (e.g., MessageSentEvent or NotificationCreatedEvent)
        event_cls = import_string(event_path)

        # 3. Instantiate the event object with its dictionary payload
        event = event_cls(**event_data)

        # 4. Fire the handler
        handler(event)
        
    except Exception as exc:
        print(f"Async execution failed for handler {handler_path}: {exc}")
        # Automatically retry utilizing your exponential backoff strategy
        countdown = self.default_retry_delay ** (self.request.retries + 1)
        raise self.retry(exc=exc, countdown=countdown)