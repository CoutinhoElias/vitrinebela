from django import template

try:
    import json as _json
except ImportError:
    import django.utils.simplejson as _json

register = template.Library()


class JsonNode(template.Node):
    def __init__(self, variable, or_null):
        self.variable = variable
        self.or_null = or_null

    def render(self, context):
        try:
            obj = self.variable.resolve(context)
        except template.VariableDoesNotExist:
            if self.or_null:
                return 'null'
            else:
                return ''
        if hasattr(obj, 'ajax_data'):
            obj = obj.ajax_data()
        return _json.dumps(obj)


@register.tag
def json(parser, token):
    '''
    {% json object %}
    {% json object or null %}
    '''
    tokens = token.split_contents()
    tag_name = tokens[0]
    values = tokens[1:]
    if len(values) not in (1, 3):
        raise template.TemplateSyntaxError(u'%r requires one or three argument.' % tag_name)
    # no compile_filter, as this does not throw VariableDoesNotExist
    variable = template.Variable(values[0])
    or_null = False
    if len(values) > 1:
        if values[1] != 'or':
            raise template.TemplateSyntaxError(u'%r second argument must be "or".' % tag_name)
        if values[2] != 'null':
            raise template.TemplateSyntaxError(u'%r third argument must be "null".' % tag_name)
        or_null = True
    return JsonNode(variable, or_null)


class AjaxCacheNode(template.Node):
    def __init__(self, variable, cache_func):
        self.variable = variable
        self.cache_func = cache_func

    def render(self, context):
        try:
            obj = self.variable.resolve(context)
            cache_func = self.cache_func.resolve(context)
        except template.VariableDoesNotExist:
            return ''
        if not hasattr(context, '_ajax_cached'):
            context._ajax_cached = {}
        if not cache_func in context._ajax_cached:
            context._ajax_cached[cache_func] = []
        if obj.pk in context._ajax_cached[cache_func]:
            return ''
        context._ajax_cached[cache_func].append(obj.pk)
        if hasattr(obj, 'ajax_data'):
            obj = obj.ajax_data()
        return u'%(cache_func)s(%(dump)s);' % {
            'cache_func': cache_func,
            'dump': _json.dumps(obj),
        }


@register.tag
def ajax_cache(parser, token):
    '''
    {% ajax_cache obj using "some_func.to.call" %}
    '''
    tokens = token.split_contents()
    tag_name = tokens[0]
    values = tokens[1:]
    if len(values) < 3:
        template.TemplateSyntaxError(u'%r requires at least one parameter.' % tag_name)
    variable = parser.compile_filter(values[0])
    if values[1] != 'using':
        template.TemplateSyntaxError(u"%r's second parameter must be 'using'." % tag_name)
    cache_func = template.Variable(values[2])
    return AjaxCacheNode(variable, cache_func)

