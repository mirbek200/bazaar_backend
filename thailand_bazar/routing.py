from django.urls import re_path

from apps.chat import consumers

websocket_urlpatterns=[
    re_path(
        r"ws/chat/(?P<chat_box_name>\w+)/$", consumers.ChatRoomConsumer.as_asgi()
    ),
    re_path(
        r"ws/user/(?P<chat_box_name>\w+)/$", consumers.User.as_asgi()
    ),
]