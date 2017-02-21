from django_ajax.config import js_context as get_js_context


def js_context(request):
    return {
        'JS_CONTEXT': get_js_context(request)
    }

