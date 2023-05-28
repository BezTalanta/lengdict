from django.template import Library
from word.models import Word

register = Library()


@register.simple_tag(takes_context=True)
def get_from_session(context, item):
    if context['request'].session.get(item, False) is True:
        return 'btn-success'
    return 'btn-danger'


@register.simple_tag(takes_context=True)
def color_word(context, id):
    if context['request'].session.get('status_color', False) is True:
        status = Word.status_getter.get_word_status(id)
        if status == 'g':
            return 'good'
        elif status == 'b':
            return 'bad'
    return ''


@register.simple_tag
def find_from_list(list, searchable_item):
    return searchable_item in list
