from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.BannerListAPIView.as_view(), name='list'),
    path('create/', views.BannerCreateAPIView.as_view(), name='create'),
    path('update_or_delete/<int:pk>/', views.BannerRetrieveUpdateDestroyAPIView.as_view(), name='update_or_delete'),
]
