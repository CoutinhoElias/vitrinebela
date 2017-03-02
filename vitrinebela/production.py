from __future__ import absolute_import, unicode_literals

from .base import *  # noqa

# AWS
# STORAGE CONFIGURATION
# ------------------------------------------------------------------------------
# Uploaded Media Files
# ------------------------
# See: http://django-storages.readthedocs.io/en/latest/index.html
INSTALLED_APPS += ['storages', ]

AWS_ACCESS_KEY_ID = config('DJANGO_AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = config('DJANGO_AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = config('DJANGO_AWS_STORAGE_BUCKET_NAME')
AWS_AUTO_CREATE_BUCKET = True
AWS_QUERYSTRING_AUTH = False
AWS_S3_CALLING_FORMAT = OrdinaryCallingFormat()

# AWS cache settings, don't change unless you know what you're doing:
AWS_EXPIRY = 60 * 60 * 24 * 7

# TODO See: https://github.com/jschneier/django-storages/issues/47
# Revert the following and use str after the above-mentioned bug is fixed in
# either django-storage-redux or boto
AWS_HEADERS = {
    'Cache-Control': six.b('max-age=%d, s-maxage=%d, must-revalidate' % (
        AWS_EXPIRY, AWS_EXPIRY))
}

# URL that handles the media served from MEDIA_ROOT, used for managing
# stored files.
#  See:http://stackoverflow.com/questions/10390244/
from storages.backends.s3boto import S3BotoStorage
StaticRootS3BotoStorage = lambda: S3BotoStorage(location='static')
MediaRootS3BotoStorage = lambda: S3BotoStorage(location='media')
DEFAULT_FILE_STORAGE = 'vitrinebela.s3utils.MediaRootS3BotoStorage'

MEDIA_URL = 'https://s3.amazonaws.com/%s/media/' % AWS_STORAGE_BUCKET_NAME


# Static Assets
# ------------------------
STATIC_URL = 'https://s3.amazonaws.com/%s/static/' % AWS_STORAGE_BUCKET_NAME
STATICFILES_STORAGE = 'vitrinebela.s3utils.StaticRootS3BotoStorage'
# See: https://github.com/antonagestam/collectfast
# For Django 1.7+, 'collectfast' should come before
# 'django.contrib.staticfiles'
AWS_PRELOAD_METADATA = True


#Thumbnails
# https://easy-thumbnails.readthedocs.io/en/2.1/ref/settings/
# THUMBNAIL_ALIASES = {
#     '': {
#         'product_image': {'size': (285, 160), 'crop': True},
#     },
#
#     '': {
#         'user_image': {'size': (50, 50), 'crop': True},
#     },
# }
# THUMBNAIL_DEFAULT_STORAGE = DEFAULT_FILE_STORAGE

#THUMBNAIL_MEDIA_URL = MEDIA_URL
#THUMBNAIL_SUBDIR = 'thumbs'

#DEFAULT_FILE_STORAGE = 'vitrinebela.production.MediaRootS3BotoStorage'
#STATICFILES_STORAGE = 'vitrinebela.production.StaticRootS3BotoStorage'


STATICFILES_STORAGE = 'myproject.s3utils.StaticS3BotoStorage'
DEFAULT_FILE_STORAGE = 'myproject.s3utils.MediaS3BotoStorage'
