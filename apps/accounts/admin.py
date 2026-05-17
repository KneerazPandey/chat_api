from django.contrib import admin
from apps.accounts.models import User, SocialProvider



admin.site.register(User)
admin.site.register(SocialProvider)
