from django.conf.urls import handler400, handler403, handler404, handler500  # noqa
from django.conf.urls.static import static
from django.conf import settings

from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

from django.contrib.sitemaps.views import sitemap
from apps.blog.sitemaps import PostSitemap


sitemaps = {
    "posts": PostSitemap,
}

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("apps.blog.urls", namespace="blog")),
    path("users/", include("apps.users.urls", namespace="users")),
    path("robots.txt", TemplateView.as_view(template_name="bunin/robots.txt")),
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler400 = "apps.shared.views.bad_request_view"  # noqa
handler403 = "apps.shared.views.page_permission_denied_view"  # noqa
handler404 = "apps.shared.views.page_not_found_view"  # noqa
handler500 = "apps.shared.views.server_error_view"  # noqa
