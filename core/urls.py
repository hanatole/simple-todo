from django.urls import path

from core import api

urlpatterns = [
    path("health", api.health, name="health"),
    path("health", api.all_todos, name="all_todos"),
]
