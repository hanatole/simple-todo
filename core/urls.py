from django.urls import path

from core import api

urlpatterns = [
    path("health", api.health, name="health")
]
