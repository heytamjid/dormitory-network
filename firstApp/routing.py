from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/active-now/', consumers.ActiveNowConsumer.as_asgi()),
]