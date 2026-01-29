from django.contrib import admin
from apps.chat.models import ChatMessage, Contact


@admin.register(ChatMessage)
class AdminChatMessage(admin.ModelAdmin):
    list_display = ("sender", "recipient", "message")


@admin.register(Contact)
class AdminContacts(admin.ModelAdmin):
    list_display = ("id", "user")
