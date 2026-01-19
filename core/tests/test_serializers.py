import pytest

from core.serializers import TodoSerializer


def test_valid_data_should_pass():
    todo = TodoSerializer(data={"title": "Test", "status": "New"})
    assert todo.is_valid()
    assert todo.validated_data["title"] == "Test"
    assert todo.validated_data["status"] == "New"


@pytest.mark.parametrize(
    "data, error_field, error_message",
    [
        ({"status": "Doing"}, "title", "This field is required."),
        ({"title": "Title", "status": "Open"}, "status", "Select a valid choice."),
    ],
)
def test_invalid_data_should_fail(data, error_field, error_message):
    todo = TodoSerializer(data=data)
    assert not todo.is_valid()
    assert todo.errors[error_field][0] == error_message
