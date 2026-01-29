from django.urls import path
from apps.events import views

urlpatterns = [
    path("create/", views.EventCreateAPIView.as_view(), name="create"),
    path("delete/<int:id_event>/", views.EventDeleteAPIView.as_view(), name="delete"),
    path("update/<int:id_event>/", views.EventUpdateAPIView.as_view(), name="update"),
    path("detail/<int:id_event>/", views.EventDetailAPIView.as_view(), name="detail"),
    path('list/', views.EventListAPIView.as_view(), name='event-list'),
    path('banned-list/', views.EventNoActivListAPIView.as_view(), name='event-no-activ-list'),
    path('on_moderation/', views.EventOnModerationListAPIView.as_view(), name='on_moderation'),
    path('pass_moderation/<int:id_event>/', views.PassedModerationAPIView.as_view(), name='pass_moderation'),
    path('hide_or_active/<int:id_event>/', views.HideOrActiveEventAPIView.as_view(), name='hide_or_active'),
]
