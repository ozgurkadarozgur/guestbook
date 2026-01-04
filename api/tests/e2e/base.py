from typing import Any

from django.test import TestCase
from rest_framework.response import Response
from rest_framework.test import APIClient


class BaseTestCase(TestCase):
    def setUp(self):
        super().setUp()

        self.http_client = APIClient()

    def send_get_request(self, path: str) -> Response:
        return self.http_client.get(path)

    def send_post_request(self, path: str, data: dict[str, Any]) -> Response:
        return self.http_client.post(path, data, "json")
