
from django.urls import path
from django.conf.urls import url

from .consumers import ChatConsumer
from . import views

app_name = 'chat'
urlpatterns = [
    path("", views.chats, name="chats"),
    path("<str:other_username>", views.chat, name="chat"),
]

websocket_urlpatterns = [
    url(r"^chat/(?P<other_username>[\w.@+-]+)$", ChatConsumer.as_asgi() )
]