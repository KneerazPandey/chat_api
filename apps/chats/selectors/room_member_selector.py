from apps.chats.models import RoomMember
from channels.db import database_sync_to_async



class RoomMemberSelector:
    @staticmethod
    @database_sync_to_async
    def check_membership(user, room_id):
        return RoomMember.objects.filter(user=user, room_id=room_id).exists()