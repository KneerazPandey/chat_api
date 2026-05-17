from rest_framework import serializers
from django.contrib.auth import get_user_model
from apps.chats.models import Room, RoomMember

User = get_user_model()

class UserMiniSerializer(serializers.ModelSerializer):
    """Minimal user data to attach to room queries."""
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name']


class RoomSerializer(serializers.ModelSerializer):
    """Serializes the Room details."""
    class Meta:
        model = Room
        fields = ['id', 'name', 'is_group', 'created_at', 'updated_at']


class CreateRoomSerializer(serializers.Serializer):
    """
    Handles room creation payloads.
    If is_group=False, 'receiver_id' is required.
    If is_group=True, 'name' is required.
    """
    is_group = serializers.BooleanField(default=False)
    name = serializers.CharField(max_length=255, required=False, allow_blank=True)
    friend_id = serializers.UUIDField(required=False, allow_null=True)

    def validate(self, attrs):
        is_group = attrs.get('is_group')
        
        if is_group and not attrs.get('name'):
            raise serializers.ValidationError({"name": "Group chats require a name."})
        
        if not is_group and not attrs.get('friend_id'):
            raise serializers.ValidationError({"friend_id": "Private 1-to-1 chats require an friend_id."})
            
        if not is_group and attrs.get('friend_id') == self.context['request'].user.id:
            raise serializers.ValidationError({"friend_id": "You cannot start a private chat with yourself."})
            
        return attrs