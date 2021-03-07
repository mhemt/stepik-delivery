from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.routers import DefaultRouter

from apps.carts.views import CartItemViewSet
from apps.items.views import ItemViewSet

router = DefaultRouter()
router.register('items', ItemViewSet, basename='item')
router.register('carts/items', CartItemViewSet, basename='cart_item')
apipatterns = router.urls

schema_view = get_schema_view(
    openapi.Info(
        title='Stepik Delivery DRF API',
        default_version='v1',
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('', include(apipatterns)),
    path('admin/', admin.site.urls, name='admin'),
    path('api/v1/docs/', schema_view.with_ui('swagger', cache_timeout=0)),
    path('carts/', include('apps.carts.urls')),
    path('users/', include('apps.users.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
