from rest_framework import serializers

from apps.admin_panel.serializers import CategorySerializer, SubCategorySerializer, UnderSubCategorySerializer
from apps.announcement.models import (
    AnnouncementImage,
    Announcement,
    Cars,
    Motorcycles,
    Mopeds,
    TransportRental,
    Transfers,
    RealEstates,
    TakeOff,
    Buy,
    ServicesCargoTransportation,
    Cloth,
    Shoes,
    Accessories,
    ProductsForChildren,
    BeautyHealth,
    Electronics,
    LookingJob,
    LookingEmployee, BannedAnnouncement
)
from apps.forbidden_words.models import ForbiddenWords
from apps.tools.serializers import CitySerializer, DistrictSerializer
from apps.users.models import MyUser


class BaseAnnouncementSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    category_title = serializers.SerializerMethodField()
    sub_category_title = serializers.SerializerMethodField()
    under_sub_category_title = serializers.SerializerMethodField()
    city_name = serializers.SerializerMethodField()
    district_name = serializers.SerializerMethodField()
    city = CitySerializer()
    district = DistrictSerializer()

    class Meta:
        abstract = True

    def get_images(self, obj):
        try:
            images = AnnouncementImage.objects.filter(announcement=obj)
            if images.exists():
                serializer = AnnouncementImageSerializer(images, many=True)
                return serializer.data
            return None
        except Exception:
            return None

    def get_category_title(self, obj):
        return obj.category.category_title if obj.category else None

    def get_sub_category_title(self, obj):
        return obj.sub_category.sub_category_title if obj.sub_category else None

    def get_under_sub_category_title(self, obj):
        return obj.under_sub_category.under_sub_category_title if obj.under_sub_category else None

    def get_city_name(self, obj):
        return obj.city.name if obj.city else None

    def get_district_name(self, obj):
        return obj.district.name if obj.district else None


class BaseDetailAnnouncementSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    category_title = serializers.SerializerMethodField()
    sub_category_title = serializers.SerializerMethodField()
    under_sub_category_title = serializers.SerializerMethodField()
    city_name = serializers.SerializerMethodField()
    district_name = serializers.SerializerMethodField()

    city = CitySerializer()
    district = DistrictSerializer()

    category = CategorySerializer()
    sub_category = SubCategorySerializer()
    under_sub_category = UnderSubCategorySerializer()

    class Meta:
        abstract = True

    def get_images(self, obj):
        try:
            images = AnnouncementImage.objects.filter(announcement=obj)
            if images.exists():
                serializer = AnnouncementImageSerializer(images, many=True)
                return serializer.data
            return None
        except Exception:
            return None

    def get_category_title(self, obj):
        return getattr(obj.category, 'category_title', None) if hasattr(obj, 'category') else None

    def get_sub_category_title(self, obj):
        return getattr(obj.sub_category, 'sub_category_title', None) if hasattr(obj, 'sub_category') else None

    def get_under_sub_category_title(self, obj):
        return getattr(obj.under_sub_category, 'under_sub_category_title', None) if hasattr(obj,
                                                                                            'under_sub_category') else None

    def get_city_name(self, obj):
        return obj.city.name if obj.city else None

    def get_district_name(self, obj):
        return obj.district.name if obj.district else None


class UserViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = MyUser
        exclude = ('password', 'is_superuser', 'is_active', 'is_staff')


class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = ['id', 'user', 'category', 'sub_category', 'under_sub_category', 'title',
                  'description', 'price', 'city', 'district', 'is_active', 'is_banned', 'address', 'longitude',
                  'latitude']

    def validate(self, data):
        title = data.get('title', '')
        description = data.get('description', '')

        forbidden_words = ForbiddenWords.objects.values_list('word', flat=True)

        words_to_check = f"{title} {description}".split()
        if any(word.lower() in words_to_check for word in forbidden_words):
            data['is_active'] = False
            data['is_banned'] = True
        else:
            data['is_active'] = True
            data['is_banned'] = False
        return data


class AnnouncementImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnnouncementImage
        fields = ['id', 'announcement', 'image']


class AnnouncementImageRequestSerializer(serializers.Serializer): # noqa
    image = serializers.ImageField()


class CreateRequestAnnouncementSerializer(serializers.Serializer):
    announcement = AnnouncementSerializer()
    images = AnnouncementImageRequestSerializer(many=True)


class AnnouncementListSerializer(BaseAnnouncementSerializer):

    class Meta:
        model = Announcement
        exclude = ['category', 'sub_category', 'under_sub_category']


class AnnouncementDetailSerializer(BaseDetailAnnouncementSerializer):
    category = CategorySerializer()
    sub_category = SubCategorySerializer()
    under_sub_category = UnderSubCategorySerializer()

    class Meta:
        model = Announcement
        fields = '__all__'


def create_announcement_serializer(model_data):
    class AnnouncementSerializer(serializers.ModelSerializer):
        class Meta:
            model = model_data
            fields = "__all__"

        def validate(self, data):
            title = data.get('title', '')
            description = data.get('description', '')

            forbidden_words = ForbiddenWords.objects.values_list('word', flat=True)

            words_to_check = f"{title} {description}".split()
            if any(word.lower() in words_to_check for word in forbidden_words):
                data['is_active'] = False
                data['is_banned'] = True
            else:
                data['is_active'] = True
                data['is_banned'] = False
            return data

    return AnnouncementSerializer


CarsSerializer = create_announcement_serializer(Cars)
MotorcyclesSerializer = create_announcement_serializer(Motorcycles)
MopedsSerializer = create_announcement_serializer(Mopeds)
TransfersSerializer = create_announcement_serializer(Transfers)
RealEstatesSerializer = create_announcement_serializer(RealEstates)
TakeOffSerializer = create_announcement_serializer(TakeOff)
BuySerializer = create_announcement_serializer(Buy)
ServicesCargoTransportationSerializer = create_announcement_serializer(ServicesCargoTransportation)
ClothSerializer = create_announcement_serializer(Cloth)
ShoesSerializer = create_announcement_serializer(Shoes)
AccessoriesSerializer = create_announcement_serializer(Accessories)
ProductsForChildrenSerializer = create_announcement_serializer(ProductsForChildren)
BeautyHealthSerializer = create_announcement_serializer(BeautyHealth)
ElectronicsSerializer = create_announcement_serializer(Electronics)
LookingJobSerializer = create_announcement_serializer(LookingJob)
LookingEmployeeSerializer = create_announcement_serializer(LookingEmployee)


class DetailListUpdateSerializer(BaseAnnouncementSerializer):
    category = CategorySerializer()
    sub_category = SubCategorySerializer()
    under_sub_category = UnderSubCategorySerializer()

    class Meta:
        abstract = True
        fields = "__all__"


def create_list_detail_serializer(model_data):
    class ListDetailSerializer(DetailListUpdateSerializer):
        class Meta(DetailListUpdateSerializer.Meta):
            model = model_data

    return ListDetailSerializer

CarsListDetailSerializer = create_list_detail_serializer(Cars)
MotorcyclesListDetailSerializer = create_list_detail_serializer(Motorcycles)
MopedsListDetailSerializer = create_list_detail_serializer(Mopeds)
TransfersListDetailSerializer = create_list_detail_serializer(Transfers)
RealEstatesListDetailSerializer = create_list_detail_serializer(RealEstates)
TakeOffListDetailSerializer = create_list_detail_serializer(TakeOff)
BuyListDetailSerializer = create_list_detail_serializer(Buy)
ServicesCargoTransportationListDetailSerializer = create_list_detail_serializer(ServicesCargoTransportation)
ClothListDetailSerializer = create_list_detail_serializer(Cloth)
ShoesListDetailSerializer = create_list_detail_serializer(Shoes)
AccessoriesListDetailSerializer = create_list_detail_serializer(Accessories)
ProductsForChildrenListDetailSerializer = create_list_detail_serializer(ProductsForChildren)
BeautyHealthListDetailSerializer = create_list_detail_serializer(BeautyHealth)
ElectronicsListDetailSerializer = create_list_detail_serializer(Electronics)
LookingJobListDetailSerializer = create_list_detail_serializer(LookingJob)
LookingEmployeeListDetailSerializer = create_list_detail_serializer(LookingEmployee)
AnnouncementListDetailUpdateSerializer = create_list_detail_serializer(Announcement)


class AnnouncementUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = ['id', 'user', 'category', 'sub_category', 'under_sub_category', 'title',
                  'description', 'price', 'city', 'district', 'is_active', 'is_banned']


class BannedAnnouncementSerializer(serializers.ModelSerializer):

    class Meta:
        model = BannedAnnouncement
        fields = "__all__"

