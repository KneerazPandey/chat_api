from rest_framework.request import Request
from rest_framework import status
from rest_framework.generics import GenericAPIView
from .serializers import (
    UserMiniSerializer, CreateRoomSerializer, RoomSerializer
)
from apps.chats.models import Room, RoomMember
from django.db.models import Count
from django.db import transaction
from core.responses import ApiResponse



class RoomCreateAPIView(GenericAPIView):
    serializer_class = CreateRoomSerializer

    def post(self, request: Request):
        serializer = self.serializer_class(
            data=request.data,
            context={
                'request': request
            }
        )
        serializer.is_valid(raise_exception=True)

        user = request.user
        is_group = serializer.validated_data['is_group']

        # --- 1-TO-1 CHAT OPTIMIZATION FLOW ---
        if not is_group:
            friend_id = serializer.validated_data['friend_id']
            # Check if a 1-to-1 room already exists between these two exact users
            # look for rooms containing both users where total member count is exactly 2
            existing_room = Room.objects.filter(
                is_group=False,
                members__user_id__in=[user.id, friend_id]
            ).annotate(
                member_count=Count('members')
            ).filter(member_count=2).first()
            if existing_room:
                # If it exists, return it instead of throwing an error or duplicating
                return ApiResponse.success(
                    message='You have already started chatting.',
                    data=RoomSerializer(existing_room).data,
                    status_code=status.HTTP_200_OK
                )
            
        # --- CREATION FLOW (Atomic Transaction to guarantee integrity) ---
        with transaction.atomic():
            room = Room.objects.create(
                is_group=is_group,
                name=serializer.validated_data.get('name', '') if is_group else None
            )

            # Add the creator to the room
            RoomMember.objects.create(room=room, user=user)

            # If it's a private chat, add the receiver right away
            if not is_group:
                RoomMember.objects.create(room=room, user_id=friend_id)

        return ApiResponse.success(
            message='Room has been successfully created.',
            data=RoomSerializer(existing_room).data,
            status_code=status.HTTP_201_CREATED
        )




class JoinGroupRoomAPIView(GenericAPIView):

    def post(self, request, room_id):
        try:
            # Enforce that you can only "Join" group chats via endpoint, not hijack private 1-to-1s
            room = Room.objects.get(id=room_id, is_group=True)
        except Room.DoesNotExist:
            return ApiResponse.error(
                message='Group room not found',
                status_code=status.HTTP_404_NOT_FOUND
            )
       
        # get_or_create prevents double-joining errors if they click the button twice
        member, created = RoomMember.objects.get_or_create(
            room=room, 
            user=request.user
        )

        if not created:
            return ApiResponse.success(
                message='You are already a member of this room',
                data={},
                status_code=status.HTTP_200_OK
            )
            

        return ApiResponse.success(
            message=f'Successfully joined group: {room.name or room.id}',
            status_code=status.HTTP_201_CREATED
        )
