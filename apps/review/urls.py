from django.urls import path
from .views import ReviewCreateView, ReviewDeleteView

app_name = 'reviews'

urlpatterns = [
    path('create/', ReviewCreateView.as_view(), name='review_create'),
    path('delete/<int:pk>/', ReviewDeleteView.as_view(), name='review_delete'),
]
