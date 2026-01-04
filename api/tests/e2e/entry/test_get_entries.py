from http import HTTPStatus
from typing import NamedTuple, Any
from unittest.mock import patch

from math import ceil

from api.tests.e2e.base import BaseTestCase


class EntryInput(NamedTuple):
    user_name: str
    subject: str
    message: str


class GetEntriesTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()

        self.mock_entry_pagination_limit = 4
        self.entries_pagination_limit_patch = patch("api.service.entry.DEFAULT_ENTRIES_PAGINATION_LIMIT", self.mock_entry_pagination_limit)
        self.entries_pagination_limit_patch.start()

        self.entry_count = 10
        self.entry_inputs = []
        for i in range(self.entry_count):
            self.entry_inputs.append(
                EntryInput(
                    user_name=f"dummy-user-name-{i}",
                    subject=f"dummy-subject-{i}",
                    message=f"dummy-message-{i}",
                )
            )

        for entry_input in self.entry_inputs:
            data = {
                "subject": entry_input.subject,
                "message": entry_input.message,
                "name": entry_input.user_name,
            }
            response = self.send_post_request("/api/entry/", data)
            self.assertEqual(response.status_code, HTTPStatus.OK)

    def tearDown(self):
        self.entries_pagination_limit_patch.stop()

        super().tearDown()

    def get_entries_request_path(self, next_link: str | None = None, previous_link: str | None = None) -> str:
        if next_link is not None:
            return next_link
        elif previous_link is not None:
            return previous_link
        else:
            return "/api/entry/"

    def assert_entries_in_page(self, page_number: int, page_size: int, entries: list[dict[str, Any]]):
        start_position = (page_number - 1) * page_size
        end_position = page_number * page_size

        entries_in_page = self.entry_inputs[::-1][start_position: end_position]

        self.assertEqual(len(entries_in_page), len(entries))

        for expected_entry, actual_entry in zip(entries_in_page, entries):
            self.assertEqual(expected_entry.user_name, actual_entry["user"]["name"])
            self.assertEqual(expected_entry.subject, actual_entry["subject"])
            self.assertEqual(expected_entry.message, actual_entry["message"])

    def test_get_entries(self):
        expected_page_count = ceil(self.entry_count / self.mock_entry_pagination_limit)
        expected_last_page_entry_count = self.entry_count % self.mock_entry_pagination_limit

        next_link = None
        previous_link = None
        page_number = 0
        for i in range(expected_page_count):
            page_number = i + 1

            response = self.send_get_request(self.get_entries_request_path(next_link, previous_link))
            self.assertEqual(response.status_code, HTTPStatus.OK)

            response_data = response.json()
            links = response_data["links"]
            next_link = links["next_link"]
            previous_link = links["previous_link"]
            entries = response_data["entries"]

            if page_number < expected_page_count:
                self.assertEqual(len(entries), self.mock_entry_pagination_limit)
            else:
                # means last page
                self.assertEqual(len(entries), expected_last_page_entry_count)

            self.assert_entries_in_page(page_number, self.mock_entry_pagination_limit, entries)

        self.assertEqual(page_number, expected_page_count)
