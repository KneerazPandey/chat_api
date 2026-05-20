from django.core.cache import cache
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.tokens import RefreshToken
from apps.accounts.selectors import UserSelector
from core.utils import Otp
from core.exceptions.errors import EmailAlreadyExistsError
from apps.accounts.events import UserRegisteredOtpRequestedEvent
from core.events.dispatcher import EventDispatcher
from asgiref.sync import async_to_sync


class AuthService:
    @staticmethod
    def register(email: str, password: str, **kwargs):
        email = email.strip().lower()
        if UserSelector.is_email_exist(email=email):
            raise EmailAlreadyExistsError()
        
        cache_key = f'auth:register:{email}'
        otp = Otp.generate_random_otp()
        data = {
            'email': email,
            'otp': otp,
            'password': make_password(password=password)
        }
        cache.set(
            cache_key,
            data,
            timeout=300
        )

        event = UserRegisteredOtpRequestedEvent(
            email=email,
            otp=otp,
        )
        async_to_sync(EventDispatcher.dispatch)(event=event)

        return otp
    
    @staticmethod
    def login(email: str, password: str) -> dict:
        email = email.strip().lower()
        user = authenticate(email=email, password=password)

        if not user:
            raise ValueError("Invalid credentials")

        refresh = RefreshToken.for_user(user)

        return {
            "user": user,
            "access": str(refresh.access_token),
            "refresh": str(refresh)
        }
        

