from django.urls import path
from apps.complaint import views

urlpatterns = [
    path("create/<int:announcements_id>/", views.CreateAnnouncementToSavedView.as_view(), name="create"),
    path("list/", views.ListAnnouncementOfSavedView.as_view(), name="list"),
    path("delete/<int:announcements_id>/", views.DeleteAnnouncementOfSavedView.as_view(), name="delete"),

    path("event_create/<int:event_id>/", views.CreateEventToSavedView.as_view(), name="create"),
    path("event_list/", views.ListEventOfSavedView.as_view(), name="list"),
    path("event_delete/<int:event_id>/", views.DeleteEventOfSavedView.as_view(), name="delete"),
]
