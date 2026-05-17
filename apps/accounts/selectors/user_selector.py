from django.contrib.auth import get_user_model

User = get_user_model()

class UserSelector:
    @staticmethod
    def is_email_exist(email: str) -> bool:
        return User.objects.filter(email=email).exists()
    