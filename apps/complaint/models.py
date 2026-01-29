from django.db import models

from apps.announcement.models import Announcement
from apps.users.models import MyUser
from apps.events.models import Event


class Saved(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE)
    announcements = models.ManyToManyField(Announcement, null=True, blank=True)

    def __str__(self):
        return f'{self.user.email}`s cart'

    def add_to_favorites_announcements(self, announcements):
        self.announcements.add(announcements)

    def remove_from_favorites_announcements(self, announcements):
        self.announcements.remove(announcements)


class SavedEvents(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE)
    event = models.ManyToManyField(Event, null=True, blank=True)

    def __str__(self):
        return f'{self.user.email}`s cart'

    def add_to_favorites_event(self, announcements):
        self.event.add(announcements)

    def remove_from_favorites_event(self, announcements):
        self.event.remove(announcements)
