from django.contrib import admin

from apps.announcement.models import (
    Announcement, AnnouncementImage,

    TransportRental,
    Cars, Motorcycles, Mopeds, Transfers,

    RealEstates,
    TakeOff, Buy, LookingEmployee, LookingJob, Electronics, BeautyHealth, ProductsForChildren, Accessories, Shoes,
    Cloth, ServicesCargoTransportation,

    BannedAnnouncement
)


@admin.register(Announcement)
class AdminAnnouncement(admin.ModelAdmin):
    list_display = ("id", "is_active")


@admin.register(AnnouncementImage)
class AdminAnnouncementImage(admin.ModelAdmin):
    list_display = ("id", "image")


@admin.register(TransportRental)
class TransportRentalAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "rental_price", "is_active", "is_banned", "created_at")


@admin.register(Cars)
class CarsAdmin(admin.ModelAdmin):
    list_display = ("id", "rental_type", "deposit", "color", "delivery", "child_seat", "phone_charger", "audio_system")


@admin.register(Motorcycles)
class MotorcyclesAdmin(admin.ModelAdmin):
    list_display = ("id", "rental_type", "deposit", "color", "delivery", "child_seat", "phone_charger", "audio_system", "engine_capacity")


@admin.register(Mopeds)
class MopedsAdmin(admin.ModelAdmin):
    list_display = ("id", "rental_type", "deposit", "color", "delivery", "phone_mount")


@admin.register(Transfers)
class TransfersAdmin(admin.ModelAdmin):
    list_display = ('id', 'vehicle_type', 'service_type', 'drive', 'child_seat', 'phone_charger', 'meeting_with_sign')


@admin.register(RealEstates)
class RealEstatesAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'type_housing', 'price_estate', 'number_of_rooms', 'swimming_pool', 'with_photo']


@admin.register(TakeOff)
class TakeOffAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'rules']


@admin.register(Buy)
class BuyAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'type_estate']


@admin.register(ServicesCargoTransportation)
class ServicesCargoTransportationAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'availability_of_loaders']


@admin.register(Cloth)
class ClothAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'gender', 'color', 'size', 'brand', 'state']


@admin.register(Shoes)
class ShoesAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'gender', 'color', 'size', 'brand', 'state']


@admin.register(Accessories)
class AccessoriesAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'state', 'color', 'brand', 'gender']


@admin.register(ProductsForChildren)
class ProductsForChildrenAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'state']


@admin.register(BeautyHealth)
class BeautyHealthAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'state']


@admin.register(Electronics)
class ElectronicsAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'state', 'color', 'manufacturer']


@admin.register(LookingJob)
class LookingJobAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'schedule', 'wage', 'experience']


@admin.register(LookingEmployee)
class LookingEmployeeAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'schedule', 'payment', 'experience', 'gender']


admin.site.register(BannedAnnouncement)