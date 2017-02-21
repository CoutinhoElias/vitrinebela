from django.core.exceptions import ImproperlyConfigured
from django.utils.importlib import import_module
from django.conf import settings

AJAX_CONFIG_PROCESSORS = getattr(settings, 'AJAX_CONFIG_PROCESSORS', ())


# TODO: Cache loaded processors
def get_config_processors(collect=AJAX_CONFIG_PROCESSORS):
    processors = []
    for path in collect:
        i = path.rfind('.')
        module, attr = path[:i], path[i + 1:]
        try:
            mod = import_module(module)
        except ImportError, e:
            raise ImproperlyConfigured('Error importing ajax config processor module %s: "%s"' % (module, e))
        try:
            func = getattr(mod, attr)
        except AttributeError:
            raise ImproperlyConfigured(
                'Module "%s" does not define a "%s" callable ajax config processor' % (module, attr))
        processors.append(func)
    return processors


def js_context(request):
    processors = get_config_processors()
    context = {}
    for processor in processors:
        context.update(processor(request))
    return context

