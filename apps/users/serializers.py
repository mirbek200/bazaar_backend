from django.core.mail import send_mail
from django.db.models import Avg
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from apps.announcement.models import Announcement
from apps.announcement.serializers import AnnouncementListSerializer
from apps.events.models import Event
from apps.events.serializers import EventListSerializer
from apps.review.models import Review
from apps.review.serializers import ReviewSerializer
from apps.users.models import MyUser
from thailand_bazar.logic.send_email import send_email_change_password


class UserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(
        write_only=True,
        required=True,
    )

    class Meta:
        model = MyUser
        fields = ['id', 'full_name', 'email', 'phone_number', 'password', 'password2']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )
        return attrs


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = None
        if '@' in data['email']:
            user = MyUser.objects.filter(email=data['email']).first()

        if user and user.check_password(data['password']):
            refresh = RefreshToken.for_user(user)
            return {
                'id': user.id,
                'email': user.email,
                'phone_number': user.phone_number,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'is_admin': user.is_admin,
                'is_superuser': user.is_superuser,
                'is_moderator': user.is_moderator,
            }
        raise serializers.ValidationError('Incorrect email or password')


class ActivationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField()

    def validate(self, data):
        email = data.get('email')
        code = data.get('code')
        if not MyUser.objects.filter(email=email, activation_code=code).exists():
            raise serializers.ValidationError('Пользователь не найден')
        return data

    def activate(self):
        email = self.validated_data.get('email')
        user = MyUser.objects.get(email=email)
        user.is_active = True
        user.activation_code = ''
        user.save()


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(min_length=6, required=True)
    new_password = serializers.CharField(min_length=6, required=True)
    new_password2 = serializers.CharField(min_length=6, required=True)

    def validate_old_password(self, old_pass):
        request = self.context.get('request')
        user = request.user
        if not user.check_password(old_pass):
            raise serializers.ValidationError('Введите верный пароль')
        return old_pass

    def validate(self, attrs):
        new_pass1 = attrs.get('new_password')
        new_pass2 = attrs.get('new_password2')
        if new_pass1 != new_pass2:
            raise serializers.ValidationError('Пароли не совпадают')
        return attrs

    def set_new_password(self):
        new_pass = self.validated_data.get('new_password')
        user = self.context.get('request').user
        user.set_password(new_pass)
        user.save()


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, email):
        if not MyUser.objects.filter(email=email).exists():
            raise serializers.ValidationError('Пользователь с указанным email не зарегистрирован')
        return email

    def send_verification_code(self):
        email = self.validated_data.get('email')
        user = MyUser.objects.get(email=email)
        user.create_activation_code()
        # send_mail(
        #     'Восстановление пароля',
        #     f'Ваш код верификации: {user.activation_code}',
        #     'test@gmail.com',
        #     [user.email]
        # )
        send_email_change_password(user)


class ForgotPasswordCompleteSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField()
    password = serializers.CharField(min_length=8)
    password2 = serializers.CharField(min_length=8)

    def validate(self, attrs):
        email = attrs.get('email')
        code = attrs.get('code')
        pass1 = attrs.get('password')
        pass2 = attrs.get('password2')
        if not MyUser.objects.filter(email=email, activation_code=code).exists():
            raise serializers.ValidationError('Пользователь не найден')
        if pass1 != pass2:
            raise serializers.ValidationError('Пароли не совпадают')
        return super().validate(attrs)

    def set_new_password(self):
        email = self.validated_data.get('email')
        password = self.validated_data.get('password')
        user = MyUser.objects.get(email=email)
        user.set_password(password)
        user.save()


class ProfileSerializer(serializers.ModelSerializer):
    announcements = serializers.SerializerMethodField()
    announcements_banned = serializers.SerializerMethodField()
    not_active_announcements = serializers.SerializerMethodField()

    events = serializers.SerializerMethodField()
    events_on_moderation = serializers.SerializerMethodField()
    events_banned = serializers.SerializerMethodField()
    not_active_events = serializers.SerializerMethodField()

    reviews = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = MyUser
        exclude = ('password', 'is_superuser', 'is_active', 'is_staff')

    def get_announcements(self, obj):
        announcements = Announcement.objects.filter(user=obj, is_active=True, is_banned=False)
        announcements_serializer = AnnouncementListSerializer(instance=announcements, many=True)
        return announcements_serializer.data

    def get_announcements_banned(self, obj):
        announcements = Announcement.objects.filter(user=obj, is_banned=True)
        announcements_serializer = AnnouncementListSerializer(instance=announcements, many=True)
        return announcements_serializer.data

    def get_not_active_announcements(self, obj):
        not_active_announcements = Announcement.objects.filter(user=obj, is_active=False, is_banned=False)
        not_active_announcements_serializer = AnnouncementListSerializer(instance=not_active_announcements, many=True)
        return not_active_announcements_serializer.data

    def get_events(self, obj):
        events = Event.objects.filter(user=obj, is_active=True, is_banned=False, on_moderation=False)
        serializer = EventListSerializer(instance=events, many=True)
        return serializer.data

    def get_events_banned(self, obj):
        events = Event.objects.filter(user=obj, is_banned=True)
        serializer = EventListSerializer(instance=events, many=True)
        return serializer.data

    def get_events_on_moderation(self, obj):
        events = Event.objects.filter(user=obj, on_moderation=True)
        serializer = EventListSerializer(instance=events, many=True)
        return serializer.data

    def get_not_active_events(self, obj):
        not_active_announcements = Event.objects.filter(user=obj, is_active=False, is_banned=False)
        not_active_announcements_serializer = EventListSerializer(instance=not_active_announcements, many=True)
        return not_active_announcements_serializer.data

    def get_reviews(self, obj):
        reviews = Review.objects.filter(recipient=obj)
        serializer = ReviewSerializer(instance=reviews, many=True)
        return serializer.data

    def get_average_rating(self, obj):
        reviews = Review.objects.filter(recipient=obj)
        average_rating = reviews.aggregate(Avg('rating'))['rating__avg']
        return round(average_rating, 2) if average_rating else 0.0


class UserViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = MyUser
        exclude = ('password', 'is_superuser', 'is_active', 'is_staff')


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['full_name', 'description', 'avatar']


class AuthorizationServiceSerializer(serializers.Serializer): # noqa
    token = serializers.CharField()


class LoginServiceSerializer(serializers.Serializer):
    email = serializers.CharField()

    def validate(self, data):
        user = None
        if '@' in data['email']:
            user = MyUser.objects.filter(email=data['email']).first()

        refresh = RefreshToken.for_user(user)
        return {
            'id': user.id,
            'email': user.email,
            'phone_number': user.phone_number,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'is_admin': user.is_admin,
            'is_superuser': user.is_superuser,
            'is_moderator': user.is_moderator,
        }


class SendReviewSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200)
    email = serializers.EmailField()
    cause = serializers.CharField(max_length=200)
    topic = serializers.CharField(max_length=1000)
