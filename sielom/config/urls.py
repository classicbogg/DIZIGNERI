from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static

from core.views import home, registration_page, healthcheck, RecordViewSet, register_team
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("records", RecordViewSet, basename="records")

urlpatterns = [
    path("", home, name="home"),
    path("registration/", registration_page, name="registration"),
    path("health/", healthcheck, name="healthcheck"),
    path("admin/", admin.site.urls),
    path("api/register-team", register_team, name="register_team"),
    path("api/", include(router.urls)),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)