"""
URL configuration for thailand_bazar project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from apps.chat.views import chat_box, ContactListView, ContactDeleteView

schema_view = get_schema_view(
    openapi.Info(
        title="My API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('apps.users.urls')),
    path('api/admin_panel/', include('apps.admin_panel.urls')),
    path('api/announcement/', include('apps.announcement.urls')),
    path('api/event/', include('apps.events.urls')),
    path('api/forbidden_words/', include('apps.forbidden_words.urls')),
    path('api/tools/', include('apps.tools.urls')),
    path("chat/<str:chat_box_name>/", chat_box, name="chat"),
    path("api/contacts/", ContactListView.as_view(), name="contacts"),
    path("api/contacts/delete/<int:id>/", ContactDeleteView.as_view(), name="contacts-delete"),
    path('api/review/', include('apps.review.urls')),
    path('api/complaint/', include('apps.complaint.urls')),
    path('api/banners/', include('apps.banners.urls')),
    path('api/complaint_system/', include('apps.complaint_system.urls')),

    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc-ui'),
]

# if settings.DEBUG:
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
