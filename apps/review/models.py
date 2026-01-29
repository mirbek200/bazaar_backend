from django.db import models
from django.utils import timezone

from apps.users.models import MyUser


class Review(models.Model):
    reviewer = models.ForeignKey(MyUser, related_name='reviews_given', on_delete=models.CASCADE)
    recipient = models.ForeignKey(MyUser, related_name='reviews_received', on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        return f"{self.reviewer.email} -> {self.recipient.email}: {self.rating}"
