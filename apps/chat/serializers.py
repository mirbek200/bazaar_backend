from rest_framework import serializers

from apps.chat.models import ChatMessage, Contact
from apps.users.serializers import UserViewSerializer


class ChatMessageSerializer(serializers.ModelSerializer):
    sender = UserViewSerializer()
    recipient = UserViewSerializer()

    class Meta:
        model = ChatMessage
        fields = ['id', 'sender', 'recipient', 'message', 'timestamp']


class ContactSerializer(serializers.ModelSerializer):
    user = UserViewSerializer()
    contacts = UserViewSerializer(many=True)

    class Meta:
        model = Contact
        fields = ['user', 'contacts']
