from django.shortcuts import render

from django.shortcuts import render
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.chat.models import Contact
from apps.chat.serializers import ContactSerializer
from apps.users.models import MyUser


def chat_box(request, chat_box_name):
    return render(request, "chat/chatbox.html", {"chat_box_name": chat_box_name})


class ContactListView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        user = request.user

        try:
            contact = Contact.objects.get(user=user)
        except Contact.DoesNotExist:
            contact = Contact.objects.create(user=user)
            contact.save()

        recent_contacts = contact.get_recent_contacts()
        serializer = ContactSerializer(instance={'user': contact.user, 'contacts': recent_contacts})
        for i in serializer.data["contacts"]:
            try:
                i['unread_count'] = contact.count_unread_messages(i["id"])
            except Exception:
                i['unread_count'] = 0

        return Response(serializer.data, status=status.HTTP_200_OK)


class ContactDeleteView(APIView):
    permission_classes = [permissions.AllowAny]

    def delete(self, request, id):
        user = request.user

        try:
            contact = Contact.objects.get(user=user)
        except Contact.DoesNotExist:
            contact = Contact.objects.create(user=user)
            contact.save()

        try:
            contact.remove_from_contacts(MyUser.objects.get(id=id))
            return Response(status=status.HTTP_204_NO_CONTENT)
        except MyUser.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

