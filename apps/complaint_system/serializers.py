from rest_framework import serializers
from .models import Complaint
from ..announcement.serializers import AnnouncementSerializer
from ..review.serializers import UserViewSerializer


class ComplaintSerializer(serializers.ModelSerializer):

    class Meta:
        model = Complaint
        fields = '__all__'


class ComplaintListSerializer(serializers.ModelSerializer):
    reviewer = UserViewSerializer()
    recipient = UserViewSerializer()
    announcement = AnnouncementSerializer()

    class Meta:
        model = Complaint
        fields = '__all__'
