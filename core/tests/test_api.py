import pytest
from django.urls import reverse
from rest_framework.test import APITestCase

from core.models import Todo


@pytest.mark.django_db
class TestApi(APITestCase):
    def test_should_pass(self):
        response = self.client.get(reverse("health"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "The TODO API is healthy!")

    def test_should_return_all_todos(self):
        payload = [
            Todo(title=title, status=status)
            for (title, status) in [("One", "Doing"), ("Two", "Done"), ("Three", "New")]
        ]
        Todo.objects.bulk_create(payload)
        response = self.client.get(reverse("todos-list"))
        self.assertEqual(response.status_code, 200)
        todos = response.json()
        self.assertEqual(len(todos), 3)
        for title, status in [("One", "Doing"), ("Two", "Done"), ("Three", "New")]:
            x = [todo for todo in todos if todo["title"] == title]
            self.assertEqual(len(x), 1)
            self.assertIsNotNone(x[0])
            self.assertIsNotNone(x[0]["id"])
            self.assertEqual(x[0]["status"], status)

    def test_should_create_todo(self):
        payload = {"title": "Test", "status": "Doing"}
        response = self.client.post(reverse("todos-list"), payload)
        self.assertEqual(response.status_code, 201)
        todo = response.json()
        self.assertIsNotNone(todo.get("id"))
        self.assertEqual(payload["status"], todo["status"])
        self.assertEqual(payload["title"], todo["title"])

    def test_should_return_400_for_invalid_data(self):
        cases = [
            ({"status": "Doing"}, "title", "This field is required."),
            ({"title": "Title", "status": "Open"}, "status", "Select a valid choice."),
        ]
        for data, error_field, error_message in cases:
            response = self.client.post(reverse("todos-list"), data)
            self.assertEqual(response.status_code, 400)
            self.assertIn(error_field, response.json())
            self.assertEqual(response.json()[error_field][0], error_message)

    def test_should_return_matching_todo(self):
        created_todo = Todo.objects.create(title="Test", status="Doing")
        response = self.client.get(
            reverse("todos-detail", kwargs={"pk": created_todo.id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["title"], created_todo.title)
        self.assertEqual(response.json()["status"], created_todo.status)

    def test_should_return_404_for_non_existing_todo(self):
        response = self.client.get(reverse("todos-detail", kwargs={"pk": 100}))
        self.assertEqual(response.status_code, 404)

    def test_should_delete_todo(self):
        created_todo = Todo.objects.create(title="Test", status="Doing")
        response = self.client.delete(
            reverse("todos-detail", kwargs={"pk": created_todo.id})
        )
        self.assertEqual(response.status_code, 204)

        response = self.client.get(
            reverse("todos-detail", kwargs={"pk": created_todo.id})
        )
        self.assertEqual(response.status_code, 404)

    def test_should_update_todo(self):
        created_todo = Todo.objects.create(title="Test", status="Doing")
        payload = {"title": "Updated", "status": "Done"}
        response = self.client.put(
            reverse("todos-detail", kwargs={"pk": created_todo.id}), payload
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["id"], created_todo.id)
        self.assertEqual(response.json()["title"], payload["title"])
