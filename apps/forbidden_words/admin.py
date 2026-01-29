from django.contrib import admin
from apps.forbidden_words.models import ForbiddenWords


@admin.register(ForbiddenWords)
class AdminForbiddenWords(admin.ModelAdmin):
    list_display = ("id",)


