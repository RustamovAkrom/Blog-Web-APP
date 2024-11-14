from functools import wraps

from django.http import HttpRequest
from django.shortcuts import render


class CustomHtmxMixin:
    def dispatch(self, request, *args, **kwargs):
        # import pdb; pdb.set_trace()
        self.template_htmx = self.template_name
        if not self.request.META.get("HTTP_HX_REQUEST"):
            self.template_name = "htmx_blog.html"
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs["template_htmx"] = self.template_htmx
        return super().get_context_data(**kwargs)


def render_htmx_or_default(template_name, htmx_template_name=None):
    def decorator(view_func):
        @wraps
        def _wrapped_view(request: HttpRequest, *args, **kwargs):
            response = view_func(request, *args, **kwargs)

            if request.headers.get("HX-Request"):
                if htmx_template_name:
                    return render(request, htmx_template_name, response.context_data)
                return render(request, template_name, response.context_data)
            return response
        return _wrapped_view
    return decorator

        