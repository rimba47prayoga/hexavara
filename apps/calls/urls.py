from rest_framework import routers

from .views import CustomerViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register('customers', CustomerViewSet, basename='customers')

urlpatterns = router.urls
