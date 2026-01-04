from http import HTTPStatus
from typing import NamedTuple
from unittest.mock import patch

from api.tests.e2e.base import BaseTestCase


class UsernameEntryCountPair(NamedTuple):
    name: str
    entry_count: int


class UsersEntryStatusesTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()

        self.mock_users_pagination_limit = 2
        self.users_pagination_limit_patch = patch("api.service.user.DEFAULT_USERS_PAGINATION_LIMIT", self.mock_users_pagination_limit)
        self.users_pagination_limit_patch.start()

        self.username_entry_counts = [
            UsernameEntryCountPair(name="dummy-user-1", entry_count=1),
            UsernameEntryCountPair(name="dummy-user-2", entry_count=2),
            UsernameEntryCountPair(name="dummy-user-3", entry_count=3),
            UsernameEntryCountPair(name="dummy-user-4", entry_count=4),
            UsernameEntryCountPair(name="dummy-user-5", entry_count=5),
        ]

        self.subject_text_prefix = "dummy-subject"
        self.message_text_prefix = "dummy-message"
        for item in self.username_entry_counts:
            for i in range(item.entry_count):
                entry_idx = i + 1

                data = {
                    "subject": f"{self.subject_text_prefix}-{entry_idx}",
                    "message": f"{self.message_text_prefix}-{entry_idx}",
                    "name": item.name,
                }
                response = self.send_post_request("/api/entry/", data)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def tearDown(self):
        self.users_pagination_limit_patch.stop()

        super().tearDown()

    def find_user_entry_status(self, username: str, users_entry_statuses: list[dict]) -> dict | None:
        return next(filter(lambda item: item["username"] == username, users_entry_statuses), None)

    def test_get_users_entry_statuses(self):
        response = self.send_get_request("/api/users/")
        self.assertEqual(response.status_code, HTTPStatus.OK)
        response_data = response.json()

        users_entry_statuses = response_data["users"]
        for item in self.username_entry_counts:
            user_entry_status = self.find_user_entry_status(item.name, users_entry_statuses)
            self.assertIsNotNone(user_entry_status)

            self.assertEqual(item.entry_count, user_entry_status["total_entry_count"])

            user_last_entry_idx = item.entry_count
            expected_user_last_entry_text = f"{self.subject_text_prefix}-{user_last_entry_idx} | {self.message_text_prefix}-{user_last_entry_idx}"
            self.assertEqual(expected_user_last_entry_text, user_entry_status["last_entry"])

