from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from users import views as user_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Securities.urls')),
    path('api/v1/datasets/', include('SecuritiesAPI.urls')),
    path('', include('users.urls')),
    path('', include('website.urls')),
]
handler404 = 'website.views.error_404_view'


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
