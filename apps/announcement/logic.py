from django.core.mail import send_mail
from rest_framework.generics import get_object_or_404

from apps.announcement.serializers import AnnouncementImageSerializer
from apps.announcement.models import AnnouncementImage


def save_images(images_data, announcement_instance):  # noqa
    for uploaded_image in images_data:
        image_data = {'image': uploaded_image, 'announcement': announcement_instance.id}
        image_serializer = AnnouncementImageSerializer(data=image_data)
        if image_serializer.is_valid():
            image_serializer.save()


def delete_images(images_data):
    for image_id in images_data:
        image = get_object_or_404(AnnouncementImage, id=image_id)
        image.delete()


def send_message(user, message):
    email = user.email
    send_mail(
        'Удалён обявление',
        f'удаление',
        'test@gmail.com',
        [email]
    )