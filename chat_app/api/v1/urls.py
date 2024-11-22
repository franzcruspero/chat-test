from django.urls import path, include
from rest_framework.routers import DefaultRouter
from chat_app.api.v1.viewsets import ConstanceViewSet

router = DefaultRouter()
router.register("", ConstanceViewSet, basename="constance")

urlpatterns = [
    path("", include(router.urls)),
]
