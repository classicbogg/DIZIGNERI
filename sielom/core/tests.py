from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from .models import Record


class AdminExportTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_superuser(
            username="admin", email="admin@example.com", password="password"
        )
        self.client = Client()
        self.client.login(username="admin", password="password")
        Record.objects.create(name="Иван", email="ivan@example.com", phone="+79990000000")

    def test_export_xlsx_response(self):
        url = reverse("admin:core_record_export_xlsx")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertIn(
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            response["Content-Type"],
        )
        self.assertIn("records_export.xlsx", response["Content-Disposition"])


class ApiAndHealthTests(TestCase):
    def test_healthcheck(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("status"), "ok")

    def test_api_requires_auth(self):
        response = self.client.get("/api/records/")
        self.assertIn(response.status_code, (401, 403))


        