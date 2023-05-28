from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
)
from django import views
from card.models import Card

from .models import Word
from .forms import WordForm


class DictView(LoginRequiredMixin, views.View):
    '''
        Show all words
    '''

    def get(self, request):
        if 'status_color' not in request.session:
            request.session['status_color'] = False

        get_all = Word.status_getter.get_filtered_objects(
            request.user,
            request.GET.get('search', False))
        return render(request, 'word/dict_page.html', {
            **get_all,
        })

    def post(self, request):
        if 'status_toggle' in request.POST:
            request.session['status_color'] = \
                not request.session['status_color']
        request.session.modifed = True
        return redirect(reverse('dict'))


class SelectDictView(views.View):

    def get(self, request):
        words_id = []
        card_id = -1
        if 'card_id' in request.GET:
            card_id = request.GET['card_id']
            card = Card.objects.get(pk=card_id)
            if card.created_by == request.user:
                words_id = [word.pk for word in card.words]
                print(words_id)
            else:
                return redirect(reverse('cards'))
        return render(request, 'word/select_dict_page.html', {
            'card_id': card_id,
            'words': Word.objects.filter(user=request.user),
            'selected_words_id': words_id,
        })

    def post(self, request):
        card_id = request.POST['card_id']
        words = []
        for k, v in request.POST.items():
            try:
                int(k)
                words.append(int(k))
            except Exception:
                pass
        if int(card_id) == -1:
            request.session['words'] = words
            request.session.modified = True
            return redirect(reverse('create_card'))
        # else:
        return redirect(reverse('select'))


class AddWordView(views.View):
    '''
        Add new word to dict by WordForm
    '''

    def get(self, request):
        return render(request, 'word/add_word_page.html', {
            'form': WordForm(),
        })

    def post(self, request):
        form = WordForm(request.POST)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            return redirect(reverse('dict'))
        form.errors['original_word'] = ['Form is invalid']
        return render(request, 'word/add_word_page.html', {
            'form': form,
        })


class WordDetail(views.View):
    '''
        Show word detail
    '''

    def get(self, request, pk):
        return render(request, 'word/word_detail_page.html', {
            'form': WordForm(instance=Word.objects.get(pk=pk)),
        })

    def post(self, request, pk):
        form = WordForm(request.POST, instance=Word.objects.get(pk=pk))
        get_button = request.POST['button']
        if get_button == 'change':
            if form.is_valid():
                form.save()
            else:
                form.errors['original_word'] = ["Form is invalid"]
                return render(request, 'word/word_detail_page.html', {
                    'form': form,
                })
        elif request.POST['button'] == 'delete':
            return redirect(reverse('word_delete', kwargs={'pk': pk}))
        return redirect(reverse('dict'))


class DeleteConfirm(views.View):
    '''
        Confirm word deletion
    '''

    def get(self, request, pk):
        return render(request, 'word/delete_confirmation_page.html', {
            'word': Word.objects.get(pk=pk)
        })

    def post(self, request, pk):
        Word.objects.get(pk=pk).delete()
        return redirect(reverse('dict'))
