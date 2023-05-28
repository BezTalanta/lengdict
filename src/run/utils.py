import random

from word.models import Word


def _parse_word(word: str):
    sep = ','
    result: dict[str, int] = {}
    if word.find(';') > -1:
        sep = ';'
    for s in word.split(sep):
        s = s.strip()
        if s != '':
            result[s] = 0
    return result


def check_word(input, orig):
    '''
        Compare two words, one from user(input) other from original word
    '''

    # Right amount is amount of right answers from user input
    # but status is amount of total answers amount,
    # every bad answers or not answered equal to -1 and vice versa
    right_amount, status = 0, 0
    input_d, orig_d = _parse_word(input), _parse_word(orig)
    for item in input_d:
        if orig_d.get(item, False) is not False:
            right_amount += 1
            orig_d[item] = 1
            input_d[item] = 1
            status += 1
        else:
            status -= 1
    for item in orig_d:
        if item == 0:
            status -= 1
    return input_d, orig_d, right_amount, status


def get_all_words_to_session(request, *args, **kwargs):
    '''
        Set all required words to session, with some additional lists for work
        amount: int:
            '' - all words
            <int> - only first words by this amount
        type:
            'w' - word only
            't' - transcription only
            'p' - percent
    '''
    words = [word.id
             for word in Word.objects.filter(user=request.user)
             if (kwargs['type'] in ['t', 'p'] and word.transcription != '') or
             (kwargs['type'] == 'w')]
    random.shuffle(words)
    amount = int(kwargs['amount']) if kwargs['amount'] != '' else len(words)
    request.session['words'] = words[:amount]
    request.session['is_word_was_shown'] = [False] * amount
    request.session['was_answer_right'] = [False] * amount
    request.session['user_input'] = [''] * amount


def get_first_word(request):
    '''
    Get first word from session
    Return index from session and original word
    '''
    for word_i, status in enumerate(request.session['is_word_was_shown']):
        if not status:
            return word_i, Word.objects.get(
                pk=request.session['words'][word_i])
    return False, False


# 'show_type', 'mm', 'sentences', 'amount', 'card'
def get_settings(request):
    request.session['run_settings'] = {}
    settings = request.session['run_settings']
    for k, v in request.POST.items():
        settings[k] = v
    get_all_words_to_session(request,
                             amount=settings['amount'],
                             type=settings['show_type'])
    request.session.modified = True


def get_from_setting(request, set_name):
    '''
        Get setting from request
        If setting is not exist it will return false
    '''
    if 'run_settings' not in request.session or \
            set_name not in request.session['run_settings']:
        return False
    return request.session['run_settings'][set_name]


def delete_settings(request):
    del request.session['words']
    del request.session['is_word_was_shown']
    del request.session['was_answer_right']
    del request.session['user_input']
    request.session.modified = True
