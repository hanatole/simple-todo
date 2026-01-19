from django.urls import path

from core import api

urlpatterns = [
    path("health", api.health, name="health"),
    path("all_todos", api.all_todos, name="all_todos"),
]
