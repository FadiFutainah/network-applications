from django.urls import path, include

from rest_framework.routers import SimpleRouter

from files.views import FileViewSet

router = SimpleRouter()

router.register('file', FileViewSet)

urlpatterns = [
    path('', include(router.urls))
]
