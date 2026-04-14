from django.http import JsonResponse
from rest_framework import permissions, viewsets

from .models import Record
from .serializers import RecordSerializer


def healthcheck(request):
    return JsonResponse({"status": "ok", "project": "DIZIGNERI"})


class RecordViewSet(viewsets.ModelViewSet):
    queryset = Record.objects.all()
    serializer_class = RecordSerializer
    permission_classes = [permissions.IsAuthenticated]