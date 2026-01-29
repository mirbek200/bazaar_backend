from django.contrib import admin
from apps.tools.models import District, City


@admin.register(District)
class AdminRegion(admin.ModelAdmin):
    list_display = ("id", "name")


@admin.register(City)
class AdminCity(admin.ModelAdmin):
    list_display = ("id", "name")

