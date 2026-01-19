from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def health(request):
    return Response({"message": "The TODO API is healthy!"}, status=200)


@api_view(['GET'])
def all_todos(request):
    return Response({"message": "All TODOs"}, status=200)
