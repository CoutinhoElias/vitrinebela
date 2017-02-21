from functools import wraps
from django.http import HttpResponse


def render_to_json(func):
    @wraps(func)
    def _render_to_json(request, *args, **kwargs):
        from django_ajax.views import render_to_json as render_to_json_view

        response = func(request, *args, **kwargs)
        if isinstance(response, HttpResponse):
            return response
        return render_to_json_view(request, response)

    return _render_to_json

