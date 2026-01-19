from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from core.models import Todo
from core.serializers import TodoSerializer


@api_view(["GET"])
def health(request):
    return Response({"message": "The TODO API is healthy!"}, status=200)


class TodoViewSet(viewsets.ModelViewSet):
    serializer_class = TodoSerializer

    def get_queryset(self):
        return Todo.objects.all()
