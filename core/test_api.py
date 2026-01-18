from django.urls import reverse
from rest_framework.test import APITestCase


class TestApi(APITestCase):

    def test_should_pass(self):
        response = self.client.get(reverse("health"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "The API is healthy!")
