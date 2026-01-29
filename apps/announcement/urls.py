from django.urls import path
from apps.announcement import views

urlpatterns = [
    path("create/", views.AnnouncementCreateAPIView.as_view(), name="create"),
    path("delete/<int:id_announcement>/", views.AnnouncementDeleteAPIView.as_view(), name="delete"),
    path("update/<int:id_announcement>/", views.AnnouncementUpdateAPIView.as_view(), name="update"),
    path("detail/<int:id_announcement>/", views.AnnouncementDetailAPIView.as_view(), name="detail"),
    path('list/', views.AnnouncementListAPIView.as_view(), name='announcement-list'),
    path('banned-list/', views.AnnouncementNoActivListAPIView.as_view(), name='announcement-no-activ-list'),
    path('search/', views.AnnouncementSearchAPIView.as_view(), name='search'),
    path("banned/<int:id>/", views.BannedAnnouncementAPIView.as_view(), name="banned"),
]
