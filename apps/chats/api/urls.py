from django.urls import path
from .views import (
    RoomCreateAPIView, JoinGroupRoomAPIView
)

urlpatterns = [
    # Payload: {"is_group": false, "friend_id": "uuid..."} OR {"is_group": true, "name": "Dev Team"}
    path('rooms/create/', RoomCreateAPIView.as_view(), name='room-create'),
    
    # URL argument takes the room's UUID directly
    path('rooms/<uuid:room_id>/join/', JoinGroupRoomAPIView.as_view(), name='room-join'),
]