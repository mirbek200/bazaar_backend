from django.urls import path
from .views import ComplaintListAPIView, ComplaintCreateAPIView, ComplaintDetailAPIView

urlpatterns = [
    path('list/', ComplaintListAPIView.as_view(), name='complaint-list'),
    path('create/', ComplaintCreateAPIView.as_view(), name='complaint-create'),
    path('detail/<int:pk>/', ComplaintDetailAPIView.as_view(), name='complaint-detail'),
]
