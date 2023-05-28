import random

from django.template import Library

from word.models import Word

register = Library()


@register.simple_tag
def get_from_list(searchable_list, index):
    return searchable_list[index]


@register.simple_tag
def get_from_dict(searchable_dict, s):
    if searchable_dict.get(s, False) is not False:
        return searchable_dict[s]
    return False


@register.simple_tag
def get_word(index):
    return Word.objects.get(id=index)


@register.simple_tag
def get_from_settings(request, searchable_str):
    settings = request.session['run_settings']
    if searchable_str in settings:
        return settings[searchable_str]
    return False


@register.simple_tag(takes_context=True)
def get_status(context, id):
    if context.request.session['is_word_was_shown'][id]:
        status = context.request.session['was_answer_right'][id]
        return 'true' if status else 'false'
    return 'not_shown'


@register.simple_tag
def percent(item):
    if random.randint(0, 1):
        return item.original_word
    return item.transcription
