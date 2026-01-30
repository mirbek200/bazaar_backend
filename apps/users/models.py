import random

from django.core.mail import send_mail
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.template.loader import render_to_string
from django.utils import timezone


class CustomUserManager(BaseUserManager):

    def create_user(self, email, phone_number, password=None, full_name=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not phone_number:
            raise ValueError('Users must have a phone number')

        user = self.model(
            email=self.normalize_email(email),
            phone_number=phone_number,
            full_name=full_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, phone_number, password, full_name=None):

        user = self.create_user(
            email=self.normalize_email(email),
            phone_number=phone_number,
            password=password,
            full_name=full_name,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser, PermissionsMixin):
    full_name = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=255, null=False, blank=False, unique=True)
    email = models.EmailField('email address', unique=True)
    password = models.CharField(max_length=255, null=False, blank=False)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    description = models.TextField(null=True, blank=True)

    activation_code = models.CharField(max_length=20, blank=True)

    is_moderator = models.BooleanField(default=False)

    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    is_banned = models.BooleanField(default=False)

    created_at = models.DateTimeField(default=timezone.now, editable=False)

    # Добавляем новые поля
    is_online = models.BooleanField(default=False)
    last_online = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number']

    objects = CustomUserManager()

    def __str__(self):
        return f'{self.email}'

    def create_activation_code(self):
        code = random.randint(100000, 999999)
        self.activation_code = code
        self.save()

    def send_activation_email(self):
        subject = 'Пожалуйста, подтвердите регистрацию / Please, confirm your registration'
        from_email = 'test@gmail.com'
        to_email = [self.email]

        context = {
            'activation_code': self.activation_code,
            'name': self.full_name,
        }

        message = render_to_string('send_email.html', context)

        send_mail(subject, message, from_email, to_email, html_message=message)
