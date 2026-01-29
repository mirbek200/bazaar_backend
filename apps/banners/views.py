from rest_framework import generics, permissions
from .models import Banners
from .serializers import BannerSerializer


class BannerListAPIView(generics.ListAPIView):
    queryset = Banners.objects.all()
    serializer_class = BannerSerializer
    permission_classes = [permissions.AllowAny]


class BannerCreateAPIView(generics.CreateAPIView):
    queryset = Banners.objects.all()
    serializer_class = BannerSerializer
    permission_classes = [permissions.IsAdminUser]


class BannerRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Banners.objects.all()
    serializer_class = BannerSerializer
    permission_classes = [permissions.IsAdminUser]
