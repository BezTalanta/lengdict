from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse
from django import views
from word.models import Word

from .utils import (
    get_first_word,
    check_word,
    get_settings,
    get_from_setting,
    delete_settings
)


# TODO: make login system and set login required mixin
class RunView(LoginRequiredMixin, views.View):
    '''
        Run view need to check user knowledge
        by type request you can define what will be using in checking
        if type starts with 'g' - that means global, like cards
        after g letter card id approaches
        if type does not start with 'g' - that means using local cards
        if type is 'd' that means full dict, and after that some options
    '''

    def get(self, request):
        if 'words' not in request.session:
            # Required menu page
            return redirect(reverse('run_menu'))
        else:
            # The next 5 lines uses for fixing bug with refreshing detail page
            # When user refreshes detail word page
            # the system takes the next word and set old input to this
            if 'see_detail' in request.session:
                request.session['is_word_was_shown'][
                    request.session['see_detail']] = True
                del request.session['see_detail']
                request.session.modified = True

            current_id, word = get_first_word(request)
            if word:
                # Render word page
                return render(request, 'run/run_word_page.html', {
                    'word': word,
                    'current_id': current_id + 1,
                    'totally_amount': len(request.session['words']),
                    'show_type': get_from_setting(request, 'show_type'),
                    'mm': get_from_setting(request, 'mm'),
                    'sentences': get_from_setting(request, 'sentences'),
                })
            else:
                # Render result page
                return redirect(reverse('run_result'))

    def post(self, request):
        # get first user's word
        ind, word = get_first_word(request)

        # get user input
        input = request.POST['input']

        # require answer uses for fixing bug with refreshing detail word page
        request.session['see_detail'] = ind

        # save user's input
        request.session['user_input'][ind] = input
        request.session.modified = True
        inp_d, orig_d, right_answers, _ = check_word(input,
                                                     word.translation)
        request.session['was_answer_right'][ind] = right_answers > 0

        # If setting affects_the_status on
        # so change word's status to calculated new
        if get_from_setting(request, 'mm'):
            word.ans_status += 1 if right_answers else -1

        return render(request, 'run/run_word_detail.html', {
            'word': word,
            'status': right_answers,
            'inp_d': inp_d,
            'orig_d': orig_d,
        })


class ResultView(LoginRequiredMixin, views.View):

    def get(self, request):
        if 'words' not in request.session:
            return redirect(reverse('run'))
        return render(request, 'run/run_result_page.html', {
            'words': request.session['words'],
            'shown': request.session['is_word_was_shown'],
            'status': request.session['was_answer_right'],
            'inputs': request.session['user_input'],
        })

    def post(self, request):
        # Clear session and start a new training
        delete_settings(request)
        return redirect(reverse('run_menu'))


class MenuView(LoginRequiredMixin, views.View):

    def get(self, request):
        return render(request, 'run/run_menu_page.html', {
            'max': Word.objects.filter(user=request.user).count(),
        })

    def post(self, request):
        get_settings(request)
        return redirect(reverse('run'))
