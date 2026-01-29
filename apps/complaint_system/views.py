from django.http import Http404
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from thailand_bazar.logic.send_email import send_to_moderator_complaint
from .models import Complaint
from .serializers import ComplaintSerializer, ComplaintListSerializer
from ..announcement.permissions import IsAdminAndModerator


class ComplaintListAPIView(APIView):
    permission_classes = [IsAdminAndModerator]

    def get(self, request):
        complaints = Complaint.objects.all()
        serializer = ComplaintListSerializer(complaints, many=True)
        return Response(serializer.data)


class ComplaintCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ComplaintSerializer

    def post(self, request):
        serializer = ComplaintSerializer(data=request.data)
        if serializer.is_valid():
            complaint = serializer.save()
            send_to_moderator_complaint(complaint.announcement_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ComplaintDetailAPIView(APIView):
    serializer_class = ComplaintSerializer
    permission_classes = [IsAdminAndModerator]

    def get_object(self, pk):
        try:
            return Complaint.objects.get(pk=pk)
        except Complaint.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        complaint = self.get_object(pk)
        serializer = ComplaintSerializer(complaint)
        return Response(serializer.data)

    def put(self, request, pk):
        complaint = self.get_object(pk)
        serializer = ComplaintSerializer(complaint, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        complaint = self.get_object(pk)
        complaint.consideration = timezone.now()
        complaint.save()
        serializer = ComplaintSerializer(complaint, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        complaint = self.get_object(pk)
        complaint.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
