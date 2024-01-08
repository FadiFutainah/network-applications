from rest_framework.routers import DefaultRouter
from files.views import FileViewSet, CheckinViewSet, CheckoutViewSet


router = DefaultRouter()

router.register('checkin', CheckinViewSet, basename='checkin')

router.register('checkout', CheckoutViewSet, basename='checkout')

router.register('file', FileViewSet, basename='file')

urlpatterns = router.urls
