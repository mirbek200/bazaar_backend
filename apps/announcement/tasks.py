from celery import shared_task
from django.utils import timezone

from thailand_bazar.logic.send_email import send_email_after_deactivate_ann
from .models import Announcement


@shared_task()
def check_announcement_expiry():

    current_datetime = timezone.now()
    thirty_days_ago = current_datetime - timezone.timedelta(days=30)

    announcements_to_update = Announcement.objects.filter(is_active=True, created_at__lt=thirty_days_ago)

    for announcement in announcements_to_update:
        announcement.is_active = False
        send_email_after_deactivate_ann(announcement.user.email)
        announcement.save()
