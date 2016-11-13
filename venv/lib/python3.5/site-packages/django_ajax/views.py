from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from django_ajax.decorators import render_to_json as render_to_json_decorator


def default_getstate(obj):
    try:
        return obj.__getstate__()
    except AttributeError:
        # TODO: Fix this, must raise exception somehow
        from django.utils.simplejson import JSONEncoder

        return JSONEncoder.default(None, obj)


def render_to_json(request, json_obj):
    try:
        import json
    except ImportError:
        import django.utils.simplejson as json

    json_string = json.dumps(json_obj, default=default_getstate)
    response = HttpResponse(json_string)
    # We support <iframe>-responses by allowing passing the iframe-param here.
    # <iframes> will not work in IE using the official mime type as the browser
    # will schow a "save file as" dialog. So <iframe>'s will be sent as
    # text/plain, which should work for other browsers, too.
    if request.REQUEST.get('iframe'):
        response['Content-Type'] = "text/plain; charset=utf-8"
    else:
        response['Content-Type'] = "application/json; charset=utf-8"
    response['Pragma'] = "no cache"
    response['Cache-Control'] = "no-cache, must-revalidate"
    return response


@render_to_json_decorator
def login(request, authentication_form=AuthenticationForm):
    status = 'ok'
    if request.method == "POST":
        form = authentication_form(data=request.POST)
        if form.is_valid():
            # Okay, security checks complete. Log the user in.
            auth_login(request, form.get_user())
            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()
            return {
                'status': status,
                'authenticated': True,
                'session_key': request.session._session_key,
            }
        else:
            status = 'failed'
    else:
        form = authentication_form(request)
    request.session.set_test_cookie()
    return {
        'status': status,
        'authenticated': False,
    }


@render_to_json_decorator
def logout(request):
    from django.contrib.auth import logout

    logout(request)
    return {
        'status': 'ok',
        'authenticated': False,
    }

