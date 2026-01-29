from rest_framework import serializers

from apps.announcement.serializers import AnnouncementSerializer
from apps.complaint.models import Saved
from apps.events.serializers import EventSerializer


class SavedSerializer(serializers.ModelSerializer):

    class Meta:
        model = Saved
        fields = '__all__'


class SavedListSerializer(serializers.ModelSerializer):
    announcements = AnnouncementSerializer(many=True, required=False)

    class Meta:
        model = Saved
        fields = '__all__'


class SavedEventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Saved
        fields = '__all__'


class SavedEventListSerializer(serializers.ModelSerializer):
    event = EventSerializer(many=True, required=False)

    class Meta:
        model = Saved
        fields = '__all__'
