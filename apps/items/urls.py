from rest_framework.routers import DefaultRouter

from apps.items.views import ItemViewSet

router = DefaultRouter()
router.register('', ItemViewSet, basename='item')
urlpatterns = router.urls
