from django.shortcuts import get_object_or_404
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from thailand_bazar.logic.send_email import send_email_added_review
from .models import Review
from .permissions import IsReviewOwner
from .serializers import ReviewSerializer, ReviewCreateSerializer
from ..users.models import MyUser


class ReviewCreateView(APIView):
    serializer_class = ReviewCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = ReviewCreateSerializer(data=request.data)
        if serializer.is_valid():
            existing_review = Review.objects.filter(
                reviewer=serializer.validated_data['reviewer'],
                recipient=serializer.validated_data['recipient']
            ).first()

            if existing_review:
                return Response({'detail': 'Review already exists for this combination.'}, status=status.HTTP_400_BAD_REQUEST)

            serializer.save()
            send_email_added_review(serializer.validated_data['recipient'])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReviewDeleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, pk, *args, **kwargs):
        user = request.user
        review = get_object_or_404(Review, id=pk)
        if review.reviewer == user:
            review.delete()
            return Response({'detail': 'Review deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_403_FORBIDDEN)
