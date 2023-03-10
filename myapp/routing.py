# chat/routing.py
from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/stock/(?P<room_name>\w+)/$", consumers.stockConsumer.as_asgi()),
]