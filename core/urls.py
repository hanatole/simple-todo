from django.urls import path
from rest_framework.routers import DefaultRouter

from core import api

router = DefaultRouter()
router.register(r"todos", api.TodoViewSet, basename="todos")

urlpatterns = [
    path("health", api.health, name="health"),
] + router.urls
