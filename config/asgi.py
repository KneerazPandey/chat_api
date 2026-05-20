"""
ASGI config for chat_api project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/asgi/
"""
import os
import django
from django.core.asgi import get_asgi_application

# 1. Setup the environment configuration first
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')

# 2. Trigger get_asgi_application() immediately
django_asgi_application = get_asgi_application()

# 3. CRITICAL: import Channels routing AFTER get_asgi_application()
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
from core.middlewares import JWTAuthMiddleware
from config.routing import websocket_urlpatterns

def JWTAuthMiddlewareStack(inner):
    return JWTAuthMiddleware(
        AuthMiddlewareStack(inner)
    )


# 4. clean ASGI pipeline
application = ProtocolTypeRouter({
    'http': django_asgi_application,
    'websocket': AllowedHostsOriginValidator(
        JWTAuthMiddlewareStack(
            URLRouter(websocket_urlpatterns)
        )
    )
})