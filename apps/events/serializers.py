from rest_framework import serializers

from apps.admin_panel.serializers import CategorySerializer, SubCategorySerializer, UnderSubCategorySerializer
from apps.events.models import Event, EventImage
from apps.forbidden_words.models import ForbiddenWords
from apps.tools.serializers import CitySerializer, DistrictSerializer
from apps.users.models import MyUser


class UserViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = MyUser
        exclude = ('password', 'is_superuser', 'is_active', 'is_staff')


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'user', 'title',
                  'description', 'price', 'max_price', 'city',
                  'phone_number', 'instagram', 'district', 'is_active', 'is_banned',
                  'event_date', 'event_time', 'event_status']

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


class EventImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventImage
        fields = ['id', 'event', 'image']


class EventImageRequestSerializer(serializers.Serializer): # noqa
    image = serializers.ImageField()


class CreateRequestEventSerializer(serializers.Serializer):
    event = EventSerializer()
    images = EventImageRequestSerializer(many=True)
    event_date = serializers.DateField(format="%d.%m.%Y")


class EventListSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    city = CitySerializer()
    district = DistrictSerializer()
    event_date = serializers.DateField(format="%d.%m.%Y")

    class Meta:
        model = Event
        fields = "__all__"

    def get_images(self, obj):
        images = EventImage.objects.filter(event=obj)
        if images.exists():
            serializer = EventImageSerializer(images, many=True)
            return serializer.data
        return None


class EventUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'user', 'title',
                  'description', 'price', 'max_price', 'city',
                  'phone_number', 'instagram', 'district', 'is_active', 'is_banned',
                  'event_date', 'event_time', 'event_status']


