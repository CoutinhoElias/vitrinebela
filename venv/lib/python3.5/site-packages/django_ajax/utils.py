from django.utils.datastructures import MultiValueDict


def jquery_to_dict(values):
    result = MultiValueDict()
    if not isinstance(values, (list, tuple, set)):
        return result
    for value in values:
        if not isinstance(value, dict):
            continue
        if 'name' in value and 'value' in value:
            result.appendlist(value['name'], value['value'])
    return result
