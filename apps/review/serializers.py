from .models import Review


from rest_framework import serializers

from ..users.models import MyUser


class UserViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = MyUser
        exclude = ('password', 'is_superuser', 'is_active', 'is_staff')


class ReviewSerializer(serializers.ModelSerializer):
    reviewer = UserViewSerializer()
    recipient = UserViewSerializer()

    class Meta:
        model = Review
        fields = ['id', 'reviewer', 'recipient', 'rating', 'comment', 'created_at']


class ReviewCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = ['id', 'reviewer', 'recipient', 'rating', 'comment']

    def validate(self, data):
        existing_review = Review.objects.filter(
            reviewer=data['reviewer'],
            recipient=data['recipient']
        ).first()

        if existing_review:
            raise serializers.ValidationError('Review already exists for this combination.')

        return data