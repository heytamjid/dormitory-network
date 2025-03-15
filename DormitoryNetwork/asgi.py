"""
ASGI config for DormitoryNetwork project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import firstApp.routing  # Replace 'your_app' with the app where your WebSocket routes will be

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # Handles traditional HTTP requests
    "websocket": AuthMiddlewareStack(
        URLRouter(
            firstApp.routing.websocket_urlpatterns
        )
    ),  # Handles WebSocket connections
})


