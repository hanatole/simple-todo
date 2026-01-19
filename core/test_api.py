from django.urls import reverse
from rest_framework.test import APITestCase


class TestApi(APITestCase):

    def test_should_pass(self):
        response = self.client.get(reverse("health"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "The TODO API is healthy!")

    def test_should_return_all_todos(self):
        response = self.client.get(reverse("all_todos"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "All TODOs")
