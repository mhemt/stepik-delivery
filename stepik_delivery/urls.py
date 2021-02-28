from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

apipatterns = [
    path('items/', include('apps.items.urls')),
]

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('api/v1/', include(apipatterns)),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
