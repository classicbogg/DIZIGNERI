import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from rest_framework import permissions, viewsets

from .models import Record, TeamApplication, TeamMember
from .serializers import RecordSerializer


def home(request):
    return render(request, "index.html")


def registration_page(request):
    return render(request, "registration.html")


def healthcheck(request):
    return JsonResponse({"status": "ok", "project": "DIZIGNERI"})


@csrf_exempt
@require_http_methods(["POST"])
def register_team(request):
    try:
        payload = json.loads(request.body.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse({"detail": "Некорректный JSON."}, status=400)

    team_name = (payload.get("team_name") or "").strip()
    course = (payload.get("course") or "").strip()
    members = payload.get("members") or []

    if not team_name:
        return JsonResponse({"detail": "Поле team_name обязательно."}, status=400)
    if not course:
        return JsonResponse({"detail": "Поле course обязательно."}, status=400)
    if not isinstance(members, list) or len(members) != 5:
        return JsonResponse({"detail": "Нужно передать ровно 5 участников."}, status=400)

    captain_count = 0
    prepared_members = []

    for idx, member in enumerate(members, start=1):
        full_name = str((member or {}).get("name") or "").strip()
        is_captain = bool((member or {}).get("is_captain"))

        if not full_name:
            return JsonResponse({"detail": f"Участник №{idx}: заполните ФИО."}, status=400)

        if is_captain:
            captain_count += 1

        prepared_members.append({"full_name": full_name, "is_captain": is_captain})

    if captain_count != 1:
        return JsonResponse({"detail": "Выберите одного капитана команды."}, status=400)

    application = TeamApplication.objects.create(team_name=team_name, course=course)
    TeamMember.objects.bulk_create(
        [
            TeamMember(
                team_application=application,
                full_name=item["full_name"],
                is_captain=item["is_captain"],
            )
            for item in prepared_members
        ]
    )

    return JsonResponse(
        {"status": "ok", "application_id": application.id, "detail": "Заявка успешно отправлена."},
        status=201,
    )


class RecordViewSet(viewsets.ModelViewSet):
    queryset = Record.objects.all()
    serializer_class = RecordSerializer
    permission_classes = [permissions.IsAuthenticated]