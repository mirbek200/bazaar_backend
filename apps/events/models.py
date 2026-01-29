from django.db import models
from django.utils import timezone

from apps.admin_panel.models import Category, SubCategory, UnderSubCategory
from apps.tools.models import City, District
from apps.users.models import MyUser


class Event(models.Model):
    user = models.ForeignKey(MyUser, verbose_name="пользовател", on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name="заголовок", blank=True, null=True)
    description = models.TextField(verbose_name="Описание", blank=True, null=True)
    price = models.IntegerField(verbose_name="цена от", default=0)
    max_price = models.IntegerField(verbose_name="цена до", null=True, blank=True)
    district = models.ForeignKey(District, verbose_name="район", on_delete=models.SET_NULL, blank=True, null=True)
    city = models.ForeignKey(City, verbose_name="город", on_delete=models.SET_NULL, blank=True, null=True)

    phone_number = models.CharField(max_length=255, verbose_name="номер телефона", blank=True, null=True)
    instagram = models.CharField(max_length=255, verbose_name="инстаграм", blank=True, null=True)

    event_status = models.CharField(max_length=255, blank=True, null=True)
    event_date = models.DateField(blank=True, null=True)
    event_time = models.TimeField(blank=True, null=True)

    is_active = models.BooleanField("Активный", default=True)
    is_banned = models.BooleanField("Запрещенный", default=False)

    on_moderation = models.BooleanField(default=True, verbose_name="На модерации")

    created_at = models.DateTimeField(default=timezone.now, editable=False)

    views = models.PositiveIntegerField(default=0, verbose_name="количество просмотров")


    class Meta:
        verbose_name = "Мероприятие"
        verbose_name_plural = "Мероприятия"
        ordering = ("id",)

    def __str__(self) -> str:
        return f"{self.id}"

    def increment_views(self):
        self.views += 1
        self.save()

    def passed_moderation(self):
        self.on_moderation = False
        self.save()

    def hide_event(self):
        self.is_active = False
        self.save()

    def active_event(self):
        self.is_active = True
        self.save()


class EventImage(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='event_images')

    class Meta:
        verbose_name = "Изображение мероприятие"
        verbose_name_plural = "Изображения мероприятия"

    def __str__(self):
        return f"Изображение {self.id} для объявления {self.event.id}"
