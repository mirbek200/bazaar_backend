import json
import os

from channels.generic.websocket import AsyncWebsocketConsumer
from django import setup
from django.db.models import Q
from django.utils import timezone

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "thailand_bazar.settings")
setup()

from thailand_bazar.logic.send_email import send_message_chat_notification

from apps.chat.serializers import ChatMessageSerializer

from rest_framework.generics import get_object_or_404

from apps.users.models import MyUser
from apps.chat.models import ChatMessage, Contact


class ChatRoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_box_name = self.scope["url_route"]["kwargs"]["chat_box_name"]
        self.recipient = self.chat_box_name.split("_")[0]
        self.sender = self.chat_box_name.split("_")[1]

        get_object_or_404(MyUser, id=self.recipient)
        get_object_or_404(MyUser, id=self.sender)

        try:
            contact = Contact.objects.get(user_id=self.sender)
        except Contact.DoesNotExist:
            contact = Contact.objects.create(user_id=self.sender)
            contact.save()

        try:
            contact_recipient = Contact.objects.get(user_id=self.recipient)
        except Contact.DoesNotExist:
            contact_recipient = Contact.objects.create(user_id=self.recipient)
            contact_recipient.save()

        contact_recipient.add_to_contacts(contact=MyUser.objects.get(id=self.sender))
        contact.add_to_contacts(contact=MyUser.objects.get(id=self.recipient))

        ChatMessage.objects.filter(
            sender_id=self.chat_box_name.split("_")[0], recipient_id=self.chat_box_name.split("_")[1], is_read=False
        ).update(is_read=True)

        previous_messages = ChatMessage.objects.filter(
            Q(sender_id=self.sender, recipient_id=self.recipient) |
            Q(sender_id=self.recipient, recipient_id=self.sender)
        ).order_by('timestamp')

        if int(self.recipient)>int(self.sender):
            self.group_name = "chat_%s" % self.recipient+"-"+self.sender
        else:
            self.group_name = "chat_%s" % self.sender + "-" + self.recipient

        await self.channel_layer.group_add(self.group_name, self.channel_name)

        await self.accept()

        for message in previous_messages:
            serializer = ChatMessageSerializer(instance=message)
            await self.send(
                text_data=json.dumps({
                    "type": "chatbox_message",
                    **serializer.data
                })
            )

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        get_object_or_404(MyUser, id=self.sender)

        chat_message = ChatMessage.objects.create(
            sender_id=self.sender, recipient_id=self.recipient, message=str(message)
        )

        serializer = ChatMessageSerializer(instance=chat_message)

        is_first_message = ChatMessage.objects.filter(
            sender_id=self.sender, recipient_id=self.recipient
        )

        if len(is_first_message)==1:
            send_message_chat_notification(self.recipient, self.sender)

        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "chatbox_message",
                "id": serializer.data["id"],
                "message": serializer.data["message"],
                "sender": serializer.data["sender"],
                "recipient": serializer.data["recipient"],
                "timestamp": serializer.data["timestamp"]
            },
        )
    # Receive message from room group.
    async def chatbox_message(self, event):

        await self.send(
            text_data=json.dumps(
                {
                    "id": event["id"],
                    "message": event["message"],
                    "sender": event["sender"],
                    "recipient": event["recipient"],
                    "timestamp": event["timestamp"]
                }
            )
        )

    def save_message_for_recipient(self, message, sender, recipient_id):
        ChatMessage.objects.create(
            sender_id=sender, recipient_id=recipient_id, message=message
        ).save()


class User(AsyncWebsocketConsumer):

    async def connect(self):
        self.chat_box_name = self.scope["url_route"]["kwargs"]["chat_box_name"]

        try:
            user = get_object_or_404(MyUser, id=self.chat_box_name)
            user.is_online = True
            user.last_online = timezone.now()
            user.save()
        except MyUser.DoesNotExist:
            await self.close()

        await self.accept()

    async def disconnect(self, close_code):
        try:
            user = MyUser.objects.get(id=self.chat_box_name)
            user.is_online = False
            user.last_online = timezone.now()
            user.save()
        except MyUser.DoesNotExist:
            pass

        await self.channel_layer.group_discard(self.chat_box_name, self.channel_name)

    async def receive(self, text_data):
        pass