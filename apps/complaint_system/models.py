from django.db import models
from django.utils import timezone

from apps.announcement.models import Announcement
from apps.users.models import MyUser


class Complaint(models.Model):
    reviewer = models.ForeignKey(MyUser, related_name='complaint_given', on_delete=models.CASCADE)
    recipient = models.ForeignKey(MyUser, related_name='complaint_received', on_delete=models.CASCADE)
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE)
    cause = models.CharField(max_length=255, blank=False, null=False)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    consideration = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=255, blank=True, null=True)

