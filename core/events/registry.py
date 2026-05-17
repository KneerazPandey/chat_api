from collections import defaultdict


class EventRegistry:
    _registry = defaultdict(list)

    @classmethod
    def register(cls, event_name: str, is_async_task: bool = True):
        """
        is_async_task=True: Hands off to Celery workers.
        is_async_task=False: Runs locally on the current web/ASGI container immediately.
        """
        def decorator(func):
            if event_name not in cls._registry:
                cls._registry[event_name] = []
                
            cls._registry[event_name].append({
                "handler": func,
                "is_async_task": is_async_task
            })
            return func
        return decorator

    @classmethod
    def get_handlers(cls, event_name: str):
        return cls._registry.get(event_name, [])