import uuid
from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()



class SocialProvider(models.Model):
    class SocialAccountProvicers(models.TextChoices):
        GOOGLE = 'google', 'Google'
        FACEBOOK = 'facebook', "Facebook"
        APPLE = 'apple', 'Apple'

    
    id = models.UUIDField(unique=True, primary_key=True, editable=False, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='social_accounts')
    
    provider = models.CharField(max_length=20, choices=SocialAccountProvicers.choices)
    provider_uid = models.CharField(max_length=255)

    # optional metadata
    extra_data = models.JSONField(default=dict, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("provider", "provider_uid")
        indexes = [
            models.Index(fields=['provider']),
            models.Index(fields=['provider_uid'])
        ]

    def __str__(self):
        return f"{self.provider} - {self.user.email}"


