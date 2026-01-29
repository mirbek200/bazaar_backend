from celery import shared_task
from django.utils import timezone

from thailand_bazar.logic.send_email import send_email_after_deactivate_event
from .models import Event


@shared_task()
def check_event_expiry():

    current_datetime = timezone.now()
    events_to_update = Event.objects.filter(is_active=True, event_date__lt=current_datetime)

    for event in events_to_update:
        event.is_active = False
        send_email_after_deactivate_event(event.user.email)
        event.save()
