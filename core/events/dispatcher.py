from .registry import EventRegistry
from .base import BaseEvent
from .tasks import execute_event_handler_async


class EventDispatcher:
    
    @staticmethod
    def dispatch(event: BaseEvent):
        # returns a list of dictionaries containing {"handler": func, "is_async_task": bool}
        handler_configs = EventRegistry.get_handlers(event_name=event.event_name)

        for config in handler_configs:
            handler = config["handler"]
            
            # 1. Check if the handler requested to remain local (e.g., for WebSockets)
            if not config["is_async_task"]:
                try:
                    handler(event)
                except Exception as e:
                    print(f"Local handler execution failed: {e}")
                continue  # Move directly to the next handler

            # 2. Otherwise, dynamically route it to Celery
            handler_path = f"{handler.__module__}.{handler.__name__}"
            event_path = f"{event.__class__.__module__}.{event.__class__.__name__}"

            execute_event_handler_async.delay(
                handler_path=handler_path,
                event_path=event_path,
                event_data=event.__dict__
            )