from django.apps import AppConfig


class ChatsConfig(AppConfig):
    name = 'apps.chats'

    def ready(self):
        from apps.chats.handlers import send_message_handler
        from apps.chats.handlers import save_message_handler
