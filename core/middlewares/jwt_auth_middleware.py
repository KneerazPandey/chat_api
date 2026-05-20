# core/middlewares.py
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from urllib.parse import parse_qs
import jwt
from django.conf import settings

User = get_user_model()


class JWTAuthMiddleware:
    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        # Extract token from query string (?token=...)
        query_string = scope.get("query_string", b"").decode("utf-8")
        query_params = parse_qs(query_string)
        token = query_params.get("token", [None])[0]

        if token:
            scope['user'] = await self.get_user_from_token(token)
        else:
            scope['user'] = AnonymousUser()

        return await self.inner(scope, receive, send)
    
    @database_sync_to_async
    def get_user_from_token(self, token):
        try:
            # 1. Decode using your project's SECRET_KEY
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            
            # 2. Extract the user identifier (your logs show "user_id": "80355c29...")
            user_id = payload.get("user_id")
            
            return User.objects.get(id=user_id)
        except (jwt.ExpiredSignatureError, jwt.DecodeError, User.DoesNotExist) as e:
            # Print the error to your terminal logs so you see EXACTLY why it failed!
            print(f"❌ JWT AUTH ERROR: {e}")
            return AnonymousUser()