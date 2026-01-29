from django.core.mail import send_mail
from rest_framework.generics import get_object_or_404

from apps.events.serializers import EventImageSerializer
from apps.events.models import EventImage


def save_images(images_data, event_instance):  # noqa
    for uploaded_image in images_data:
        image_data = {'image': uploaded_image, 'event': event_instance.id}
        image_serializer = EventImageSerializer(data=image_data)
        if image_serializer.is_valid():
            image_serializer.save()


def delete_images(images_data):
    for image_id in images_data:
        image = get_object_or_404(EventImage, id=image_id)
        image.delete()


def send_message(user, message):
    email = user.email
    send_mail(
        'Удалён обявление',
        f'удаление',
        'test@gmail.com',
        [email]
    )