from django.contrib.auth import get_user_model
from django.core.cache import cache
from core.exceptions import (
    RegistrationOtpCacheExpiredOrInvalidError, OtpAttemptExceedError, InvalidOtpError
)


User = get_user_model()


class VerificationService:
    
    @staticmethod
    def verify_register_otp_with_user_creation(email: str, otp: str):
        email = email.lower().strip()
        cache_key = f'auth:register:{email}'
        data = cache.get(cache_key)

        if not data:
            raise RegistrationOtpCacheExpiredOrInvalidError()
        
        attempts = data.get('attempts', 0)
        if attempts > 3:
            cache.delete(cache_key)
            raise OtpAttemptExceedError()

        if data["otp"] != otp:
            data["attempts"] = data.get("attempts", 1) + 1
            cache.set(cache_key, data, timeout=300)
            raise InvalidOtpError()
        

        user = User.objects.create(
            email=email,
            password=data["password"],
            is_verified=True
        )

        cache.delete(cache_key)

        return user 
        


