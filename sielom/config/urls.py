from django.conf import settings
from django.contrib import admin
from django.urls import path
from rest_framework.routers import DefaultRouter
from django.views.generic import TemplateView
from . import views
from config import views

from core.views import RecordViewSet, healthcheck

router = DefaultRouter()
router.register("records", RecordViewSet, basename="records")

urlpatterns = [
    path("", views.home, name="home"),
    path("registration/", TemplateView.as_view(template_name="registration.html"), name="registration"),
    path("health/", views.healthcheck, name="healthcheck"),
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns