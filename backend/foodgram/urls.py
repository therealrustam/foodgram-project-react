"""
Создание корневого маршрутизатора Foodgram проекта.
"""

from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from foodgram import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
]

if settings.DEBUG:
    urlpatterns = (
        urlpatterns +
        static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) +
        static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    )
