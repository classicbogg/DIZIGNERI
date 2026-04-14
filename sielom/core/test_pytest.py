import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

from core.models import Record, TeamApplication


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


@pytest.mark.django_db
def test_register_team_endpoint(client):
    payload = {
        "team_name": "DIZIGNERI Team",
        "course": "2 курс",
        "members": [
            {"name": "Иван Иванов", "is_captain": True},
            {"name": "Петр Петров", "is_captain": False},
            {"name": "Сидор Сидоров", "is_captain": False},
            {"name": "Анна Антонова", "is_captain": False},
            {"name": "Мария Марина", "is_captain": False},
        ],
    }

    response = client.post(
        reverse("register_team"),
        data=payload,
        content_type="application/json",
    )

    assert response.status_code == 201
    assert TeamApplication.objects.count() == 1