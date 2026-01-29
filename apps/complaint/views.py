from django.shortcuts import render, get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.announcement.models import Announcement
from apps.complaint.models import Saved, SavedEvents
from apps.complaint.serializers import SavedSerializer, SavedListSerializer, SavedEventSerializer, \
    SavedEventListSerializer
from apps.events.models import Event


class CreateAnnouncementToSavedView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        request_body=SavedSerializer(),
        responses={201: "Created successfully", 400: "Bad Request"},
        operation_description="Create an announcement to saved"
    )
    def post(self, request, announcements_id, *args, **kwargs):
        user = request.user
        try:
            saved = Saved.objects.get(user=user)
        except Saved.DoesNotExist:
            saved = Saved(user=user)
            saved.save()
        announcements = get_object_or_404(Announcement, id=announcements_id)
        saved.add_to_favorites_announcements(announcements)
        return Response(status=status.HTTP_201_CREATED)


class ListAnnouncementOfSavedView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        responses={200: "Get successfully", 400: "Bad Request"},
    )
    def get(self, request, *args, **kwargs):
        user = request.user
        saved = Saved.objects.filter(user=user)
        serializer = SavedListSerializer(saved, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DeleteAnnouncementOfSavedView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        responses={204: "Deleted", 400: "Bad Request"},
    )
    def delete(self, request, announcements_id, *args, **kwargs):
        user = request.user
        saved = Saved.objects.get(user=user)
        announcements = get_object_or_404(Announcement, id=announcements_id)
        saved.remove_from_favorites_announcements(announcements)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CreateEventToSavedView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        request_body=SavedEventSerializer(),
        responses={201: "Created successfully", 400: "Bad Request"},
        operation_description="Create an event to saved"
    )
    def post(self, request, event_id, *args, **kwargs):
        user = request.user
        try:
            saved = SavedEvents.objects.get(user=user)
        except SavedEvents.DoesNotExist:
            saved = SavedEvents(user=user)
            saved.save()
        event = get_object_or_404(Event, id=event_id)
        saved.add_to_favorites_event(event)
        return Response(status=status.HTTP_201_CREATED)


class ListEventOfSavedView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        responses={200: "Get successfully", 400: "Bad Request"},
    )
    def get(self, request, *args, **kwargs):
        user = request.user
        saved = SavedEvents.objects.filter(user=user)
        serializer = SavedEventListSerializer(saved, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DeleteEventOfSavedView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        responses={204: "Deleted", 400: "Bad Request"},
    )
    def delete(self, request, event_id, *args, **kwargs):
        user = request.user
        saved = SavedEvents.objects.get(user=user)
        event = get_object_or_404(Event, id=event_id)
        saved.remove_from_favorites_event(event)
        return Response(status=status.HTTP_204_NO_CONTENT)
