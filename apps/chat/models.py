from django.db import models
from django.db.models import Max

from apps.users.models import MyUser


class Contact(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE)
    contacts = models.ManyToManyField(MyUser, related_name='contacts')

    def add_to_contacts(self, contact):
        self.contacts.add(contact)

    def remove_from_contacts(self, contact):
        self.contacts.remove(contact)

    def get_recent_contacts(self):
        return MyUser.objects.filter(
            id__in=self.contacts.values_list('id', flat=True)
        ).annotate(
            last_message_time=Max('received_messages__timestamp')
        ).order_by('-last_message_time')

    def count_unread_messages(self, contact):
        return ChatMessage.objects.filter(
            sender=contact, recipient=self.user, is_read=False
        ).count()


class ChatMessage(models.Model):
    sender = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='received_messages')
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.id}'

    class Meta:
        ordering = ['-timestamp']