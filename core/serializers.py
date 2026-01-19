from rest_framework import serializers

from core.models import Todo


class TodoSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Todo
        fields = ("id", "title", "status")
        extra_kwargs = {
            "status": {
                "error_messages": {
                    "invalid_choice": "Select a valid choice.",
                }
            }
        }
