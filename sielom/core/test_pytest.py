import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

from core.models import Record


@pytest.mark.django_db
def test_record_api_list_requires_auth(client):
    response = client.get("/api/records/")
    assert response.status_code in (401, 403)


@pytest.mark.django_db
def test_admin_export_button_endpoint(client):
    user = get_user_model().objects.create_superuser("admin2", "admin2@example.com", "password")
    client.force_login(user)
    Record.objects.create(name="Анна", email="anna@example.com")

    response = client.get(reverse("admin:core_record_export_xlsx"))
    assert response.status_code == 200