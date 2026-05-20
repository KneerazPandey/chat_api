from django.urls import path
from apps.chats.consumers import ChatConsumer


websocket_urlpatterns = [
    path('ws/chat/<uuid:room_id>/', ChatConsumer.as_asgi(), name='chat'),
]