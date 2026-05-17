from rest_framework.request import Request
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.generics import GenericAPIView
from apps.accounts.api.serializers import (
    UserRegistrationSerializer, UserLoginSerializer
)
from apps.accounts.services import AuthService
from core.responses import ApiResponse



class UserRegistrationAPIView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserRegistrationSerializer

    def post(self, request: Request, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        otp = AuthService.register(
            email=serializer.validated_data['email'],
            password=serializer.validated_data['password']
        )

        return ApiResponse.success(
            message="Otp has been sent to your email address.",
            data={
                "email": serializer.validated_data['email'],
                "otp": otp
            },
            status_code=status.HTTP_200_OK
        )
        


class UserLoginAPIView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

    def post(self, request: Request, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        otp = AuthService.register(
            email=serializer.validated_data['email'],
            password=serializer.validated_data['password']
        )

        return ApiResponse.success(
            message="Otp has been sent to your email address.",
            data={
                "email": serializer.validated_data['email'],
                "otp": otp
            },
            status_code=status.HTTP_200_OK
        )
