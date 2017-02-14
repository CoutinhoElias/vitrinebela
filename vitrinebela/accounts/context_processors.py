# coding: utf-8
from django.contrib.staticfiles.templatetags.staticfiles import static

def user_image_url(request):
    if request.user.is_authenticated and request.user.image:
        return {'USER_IMAGE_URL': request.user.image.url}
    else:
        return {'USER_IMAGE_URL': static('materialize/img/joao.png')}

    return context 
