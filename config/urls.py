from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from core.views import RecordViewSet, healthcheck

router = DefaultRouter()
router.register("records", RecordViewSet, basename="records")

urlpatterns = [
    path("", healthcheck, name="healthcheck"),
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns