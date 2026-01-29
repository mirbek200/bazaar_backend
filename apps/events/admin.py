from django.contrib import admin
from apps.events.models import Event, EventImage


@admin.register(Event)
class AdminEvent(admin.ModelAdmin):
    list_display = ("id", "is_active")


@admin.register(EventImage)
class AdminEventImage(admin.ModelAdmin):
    list_display = ("id", "image")

