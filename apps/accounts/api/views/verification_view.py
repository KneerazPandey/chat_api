from rest_framework.request import Request
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.generics import GenericAPIView
from apps.accounts.api.serializers import VerifyRegistrationOTPSerializer
from apps.accounts.services import VerificationService
from core.responses import ApiResponse



class VerifyRegistrationOTPAPIView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = VerifyRegistrationOTPSerializer

    def post(self, request: Request, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        VerificationService.verify_register_otp_with_user_creation(
            email=serializer.validated_data['email'],
            otp=serializer.validated_data['otp']
        )

        return ApiResponse.success(
            message="Email verified successfully.",
            data={
                "email": serializer.validated_data['email'],
            },
            status_code=status.HTTP_201_CREATED
        )
    
