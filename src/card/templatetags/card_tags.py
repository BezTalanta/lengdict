from django import template


register = template.Library()


@register.simple_tag
def find_from_list(input_list, object):
    pass
