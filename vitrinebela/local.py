from __future__ import absolute_import, unicode_literals

from .base import *  # noqa

ALLOWED_HOSTS = set(ALLOWED_HOSTS + ['127.0.0.1', 'localhost'])

try:
    import debug_toolbar
except Exception:
    pass
else:
    INSTALLED_APPS = INSTALLED_APPS + (
        'debug_toolbar',
    )
    MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware', ]
    INTERNAL_IPS = ['127.0.0.1', '10.0.2.2', ]
    DEBUG_TOOLBAR_CONFIG = {
    'DISABLE_PANELS': [
        'debug_toolbar.panels.redirects.RedirectsPanel',
    ],
    'SHOW_TEMPLATE_CONTEXT': True,
    }


TEMPLATES[0]['OPTIONS']['debug'] = DEBUG
