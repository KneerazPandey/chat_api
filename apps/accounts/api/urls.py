from django.urls import path
from apps.accounts.api.views.auth_view import UserRegistrationAPIView, UserLoginAPIView
from apps.accounts.api.views.verification_view import VerifyRegistrationOTPAPIView


urlpatterns = [
    path('register/', UserRegistrationAPIView.as_view(), name='register'),

    path('login/', UserLoginAPIView.as_view(), name='login'),

    path('verify-register-otp/', VerifyRegistrationOTPAPIView.as_view(), name='verify_register_otp'),
]