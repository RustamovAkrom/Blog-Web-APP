from django.conf.urls import handler400, handler403, handler404, handler500
from django.conf.urls.static import static
from . import settings

from django.contrib import admin
from django.urls import path, include

urlpatterns = [path("admin/", admin.site.urls), path("", include("apps.blog.urls"))]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# handler400 = "apps.shared.views.bad_request_view"
# handler403 = "apps.shared.views.page_permission_denied_view"
# handler404 = "apps.shared.views.page_not_found_view"
# handler500 = "apps.shared.views.server_error_view"
