from django.db import models
from django.utils import timezone
from model_utils.managers import InheritanceManager

from apps.admin_panel.models import Category, SubCategory, UnderSubCategory
from apps.tools.models import City, District
from apps.users.models import MyUser


class Announcement(models.Model):
    user = models.ForeignKey(MyUser, verbose_name="пользовател", on_delete=models.CASCADE)
    category = models.ForeignKey(Category, verbose_name="категория", on_delete=models.SET_NULL, blank=True, null=True)
    sub_category = models.ForeignKey(SubCategory, verbose_name="суб категория", on_delete=models.SET_NULL, blank=True, null=True)
    under_sub_category = models.ForeignKey(UnderSubCategory, verbose_name="андер суб категория", on_delete=models.SET_NULL, blank=True, null=True)
    title = models.CharField(max_length=255, verbose_name="заголовок", blank=True, null=True)
    description = models.TextField(verbose_name="Описание", blank=True, null=True)
    price = models.IntegerField(verbose_name="цена", default=0)
    district = models.ForeignKey(District, verbose_name="район", on_delete=models.SET_NULL, blank=True, null=True)
    city = models.ForeignKey(City, verbose_name="город", on_delete=models.SET_NULL, blank=True, null=True)

    address = models.CharField(max_length=255, null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)

    is_active = models.BooleanField("Активный", default=True)
    is_banned = models.BooleanField("Запрещенный", default=False)

    created_at = models.DateTimeField(default=timezone.now, editable=False)

    views = models.PositiveIntegerField(default=0, verbose_name="количество просмотров")

    objects = InheritanceManager()

    class Meta:
        verbose_name = "Объявление"
        verbose_name_plural = "Объявлении"
        ordering = ("id",)

    def __str__(self) -> str:
        return f"{self.id}"

    def increment_views(self):
        self.views += 1
        self.save()


class AnnouncementImage(models.Model):
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='announcement_images')

    class Meta:
        verbose_name = "Изображение объявления"
        verbose_name_plural = "Изображения объявлений"

    def __str__(self):
        return f"Изображение {self.id} для объявления {self.announcement.id}"


#  ________   Аренда транспорта   _________
class TransportRental(Announcement):
    rental_price = models.DecimalField(verbose_name="цена аренды", max_digits=10, decimal_places=2, default=0)


class Cars(TransportRental):

    rental_type = models.CharField(
        verbose_name="Тип аренды", max_length=50, default=None, blank=True, null=True)
    deposit = models.BooleanField(
        verbose_name="Депозит", default=None, null=True, blank=True)
    color = models.CharField(
        max_length=255, blank=True, null=True)
    delivery = models.BooleanField(
        verbose_name="Доставка", default=None, null=True, blank=True,)
    child_seat = models.BooleanField(
        verbose_name="Детское кресло", default=False,)
    phone_charger = models.BooleanField(
        verbose_name="Зарядное устройство для телефона", default=False)
    audio_system = models.BooleanField(
        verbose_name="Аудиосистема", default=False)


class Motorcycles(TransportRental):

    rental_type = models.CharField(
        verbose_name="Тип аренды", max_length=50, default=None, blank=True, null=True)
    deposit = models.BooleanField(
        verbose_name="Депозит", default=None, null=True, blank=True)

    color = models.CharField(max_length=255, blank=True, null=True)
    delivery = models.BooleanField(
        verbose_name="Доставка", default=None, null=True, blank=True)

    child_seat = models.BooleanField(
        verbose_name="Детское кресло", default=False)
    phone_charger = models.BooleanField(
        verbose_name="Зарядное устройство для телефона", default=False)
    audio_system = models.BooleanField(
        verbose_name="Аудиосистема", default=False)
    engine_capacity = models.PositiveIntegerField(
        verbose_name="Объем двигателя, см³", default=None, null=True, blank=True)


class Mopeds(TransportRental):
    rental_type = models.CharField(
        verbose_name="Тип аренды", max_length=50, default=None, blank=True, null=True)

    deposit = models.BooleanField(
        verbose_name="Депозит", default=None, null=True, blank=True)

    color = models.CharField(max_length=255, blank=True, null=True)
    delivery = models.BooleanField(
        verbose_name="Доставка", default=None, null=True, blank=True)

    phone_mount = models.BooleanField(
        verbose_name="Крепление для телефона", default=False)


class Transfers(TransportRental):
    vehicle_type = models.CharField(
        verbose_name="Вид транспорта", max_length=50, blank=True, null=True, default=None)
    service_type = models.CharField(
        verbose_name="Вид услуги", max_length=50, blank=True, null=True, default=None)
    drive = models.CharField(
        verbose_name="Поездка", max_length=50, blank=True, null=True, default=None)
    child_seat = models.BooleanField(
        verbose_name="Детское кресло", default=False)
    phone_charger = models.BooleanField(
        verbose_name="Зарядное устройство для телефона", default=False)
    meeting_with_sign = models.BooleanField(
        verbose_name="Встреча с табличкой", default=False)


# Недвижимость
class RealEstates(Announcement):
    type_housing = models.CharField(verbose_name="Тип жилья", max_length=50, blank=True, null=True, default=None)
    price_estate = models.DecimalField(verbose_name="Стоимость", max_digits=10, decimal_places=2, default=0)
    number_of_rooms = models.CharField(verbose_name="Количество комнат", blank=True, null=True, max_length=255)
    swimming_pool = models.BooleanField(verbose_name="Наличие бассейна", default=False)
    with_photo = models.BooleanField(verbose_name="Объявление с фото", default=False)


class TakeOff(RealEstates):
    rules = models.CharField(verbose_name="Правила", max_length=50, blank=True, null=True)


class Buy(RealEstates):
    type_estate = models.CharField(verbose_name="Тип недвижимость", max_length=50, blank=True, null=True, default=None)


# Услуги
class ServicesCargoTransportation(Announcement):
    availability_of_loaders = models.BooleanField(verbose_name="Наличие грузчиков", default=False, blank=True, null=True)


# Личные вещи
class Cloth(Announcement):
    type_of_cloth = models.CharField(
        verbose_name="Тип одежды", max_length=50, default=None, blank=True, null=True)
    gender = models.CharField(verbose_name="Пол", max_length=50, blank=True, null=True)
    color = models.CharField(max_length=255, blank=True, null=True)
    size = models.CharField(verbose_name="Размер", max_length=25, blank=True, null=True)
    brand = models.CharField(verbose_name="Бренд", max_length=100, blank=True, null=True)
    state = models.CharField(verbose_name="Состояние", max_length=50, blank=True, null=True)


class Shoes(Announcement):
    type_of_shoes = models.CharField(
        verbose_name="Тип обуви", max_length=50, default=None, blank=True, null=True)
    gender = models.CharField(verbose_name="Пол", max_length=50, blank=True, null=True)
    color = models.CharField(max_length=255, blank=True, null=True)
    size = models.CharField(verbose_name="Размер", max_length=25, blank=True, null=True)
    brand = models.CharField(verbose_name="Бренд", max_length=100, blank=True, null=True)
    state = models.CharField(verbose_name="Состояние", max_length=50, blank=True, null=True)


class Accessories(Announcement):
    type_of_accessories = models.CharField(
        verbose_name="Тип Аксесуаров", max_length=50, default=None, blank=True, null=True)
    state = models.CharField(verbose_name="Состояние", max_length=50, blank=True, null=True)
    color = models.CharField(max_length=255, blank=True, null=True)
    brand = models.CharField(verbose_name="Бренд", max_length=100, blank=True, null=True)
    gender = models.CharField(verbose_name="Пол", max_length=50, blank=True, null=True)


class ProductsForChildren(Announcement):
    state = models.CharField(verbose_name="Состояние", max_length=50, blank=True, null=True)


class BeautyHealth(Announcement):
    state = models.CharField(verbose_name="Состояние", max_length=50, blank=True, null=True)


class Electronics(Announcement):
    type_electronic = models.CharField(verbose_name="Тип электроники", max_length=50, blank=True, null=True, default=None)
    state = models.CharField(verbose_name="Состояние", max_length=50, blank=True, null=True)
    color = models.CharField(max_length=255, blank=True, null=True)
    manufacturer = models.CharField(verbose_name="Производитель", max_length=50, blank=True, null=True)


class LookingJob(Announcement):
    schedule = models.CharField(verbose_name="График работы", max_length=50, blank=True, null=True)
    wage = models.IntegerField(verbose_name="Заработная плата", default=0, blank=True, null=True)
    experience = models.CharField(verbose_name="Опыт работы", max_length=50, blank=True, null=True)


class LookingEmployee(Announcement):
    schedule = models.CharField(verbose_name="График работы", max_length=50, blank=True, null=True)
    payment = models.CharField(verbose_name="Оплата", max_length=50, blank=True, null=True)
    experience = models.CharField(verbose_name="Опыт работы", max_length=50, blank=True, null=True)
    gender = models.CharField(verbose_name="Пол", max_length=50, blank=True, null=True)


class BannedAnnouncement(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.SET_NULL, null=True)
    announcement = models.OneToOneField(Announcement, on_delete=models.CASCADE)
    cause = models.CharField(max_length=255, blank=False, null=False)
    created_at = models.DateTimeField(default=timezone.now, editable=False)