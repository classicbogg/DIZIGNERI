from django.http import JsonResponse
from django.shortcuts import render

def healthcheck(request):
    return JsonResponse({"status": "ok", "project": "DIZIGNERI"})

def home(request):
    return render(request, "home.html")  