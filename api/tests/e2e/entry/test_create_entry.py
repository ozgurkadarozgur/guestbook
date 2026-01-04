from http import HTTPStatus

from api import models
from api.tests.e2e.base import BaseTestCase


class CreateEntryTestCase(BaseTestCase):

    def test_create_enty_with_invalid_subject(self):
        data = {
            "subject": None,
            "message": "dummy-message",
            "name": "dummy-user-name",
        }
        response = self.send_post_request("/api/entry/", data)
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

        data = {
            "subject": "",
            "message": "dummy-message",
            "name": "dummy-user-name",
        }
        response = self.send_post_request("/api/entry/", data)
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_create_enty_with_invalid_message(self):
        data = {
            "subject": "dummy-subject",
            "message": None,
            "name": "dummy-user-name",
        }
        response = self.send_post_request("/api/entry/", data)
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

        data = {
            "subject": "dummy-subject",
            "message": "",
            "name": "dummy-user-name",
        }
        response = self.send_post_request("/api/entry/", data)
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_create_enty_with_invalid_user_name(self):
        data = {
            "subject": "dummy-subject",
            "message": "dummy-message",
            "name": None,
        }
        response = self.send_post_request("/api/entry/", data)
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

        data = {
            "subject": "dummy-subject",
            "message": "dummy-message",
            "name": "",
        }
        response = self.send_post_request("/api/entry/", data)
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_create_entry(self):
        all_entries = list(models.Entry.objects.all())
        self.assertEqual(len(all_entries), 0)

        user_name = "dummy-user-name"
        subject = "dummy-subject"
        message = "dummy-message"

        data = {
            "subject": subject,
            "message": message,
            "name": user_name,
        }
        response = self.send_post_request("/api/entry/", data)
        self.assertEqual(response.status_code, HTTPStatus.OK)

        user = models.User.objects.filter(name=user_name).first()
        self.assertIsNotNone(user)

        user_entries = list(models.Entry.objects.filter(user_id=user.id).all())
        self.assertEqual(len(user_entries), 1)

        user_entry = user_entries[0]
        self.assertEqual(user_entry.subject, subject)
        self.assertEqual(user_entry.message, message)

    def test_create_entries_with_same_user_name(self):
        user_count_before_create_entries = models.User.objects.count()
        self.assertEqual(user_count_before_create_entries, 0)

        entry_count = 3

        user_name = "dummy-user-name"
        subject = "dummy-subject"
        message = "dummy-message"

        for i in range(entry_count):
            data = {
                "subject": f"{subject} - {i}",
                "message": f"{message} - {i}",
                "name": user_name,
            }
            response = self.send_post_request("/api/entry/", data)
            self.assertEqual(response.status_code, HTTPStatus.OK)

        user_count_after_create_entries = models.User.objects.count()
        self.assertEqual(user_count_after_create_entries, 1)

        user = models.User.objects.first()
        self.assertEqual(user.name, user_name)

    def test_create_entries_with_different_user_names(self):
        user_count_before_create_entries = models.User.objects.count()
        self.assertEqual(user_count_before_create_entries, 0)

        entry_count = 3

        user_name = "dummy-user-name"
        subject = "dummy-subject"
        message = "dummy-message"

        entry_user_names = []
        for i in range(entry_count):
            entry_user_name = f"{user_name} - {i}"
            data = {
                "subject": f"{subject} - {i}",
                "message": f"{message} - {i}",
                "name": entry_user_name,
            }
            response = self.send_post_request("/api/entry/", data)
            self.assertEqual(response.status_code, HTTPStatus.OK)

            entry_user_names.append(entry_user_name)

        user_count_after_create_entries = models.User.objects.count()
        self.assertEqual(user_count_after_create_entries, len(entry_user_names))

        for entry_user_name in entry_user_names:
            self.assertTrue(models.User.objects.filter(name=entry_user_name).exists())
