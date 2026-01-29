from django.urls import path
from apps.tools import views

urlpatterns = [
    path('create/', views.CreateCityWithDistrictsAPIView.as_view(), name="create"),
    path('update/<int:city_id>/', views.UpdateCityWithDistrictAPIView.as_view(), name="update"),
    path('active_cities_and_districts/', views.ActiveCitiesAndDistrictsAPIView.as_view(),
         name='active_cities_and_districts'),
    path('not_active_cities_and_districts/', views.NotActiveCitiesAndDistrictsAPIView.as_view(),
         name='not_active_cities_and_districts'),
    path('update_city/<int:pk>/', views.CityUpdateView.as_view(), name='update_city'),
    path('update_district/<int:pk>/', views.DistrictUpdateAPIView.as_view(), name='update_district'),

    path('delete_city/<int:pk>/', views.CityDeleteAPIView.as_view(), name='delete_city'),
    path('delete_district/<int:pk>/', views.DistrictDeleteAPIView.as_view(), name='delete_district'),
]
