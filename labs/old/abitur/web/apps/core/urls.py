from apps.accounts import urls as accounts_urls  # type: ignore
from apps.applicants import urls as applicants_urls
from apps.applications import urls as applications_urls
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from . import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include(accounts_urls)),
    path("applicants/", include(applicants_urls)),
    path("applications/", include(applications_urls)),
    path("", views.home, name="root"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls)),
    ] + urlpatterns
