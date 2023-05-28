from django.shortcuts import render, redirect
from django.urls import reverse
from django import views
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator

from .models import Card
from word.models import Word
from .forms import CardForm


class CardListAll(views.View):

    def get(self, request):
        l_cards = []
        if not request.user.is_anonymous:
            l_cards = Card.objects.filter(
                created_by=get_user_model().objects.get(pk=request.user.pk)),
        g_cards = Card.objects.filter(is_global=True)

        l_page_num = request.GET.get('l_page_num', 1)
        g_page_num = request.GET.get('g_page_num', 1)

        l_cards = Paginator(l_cards[0], 5).get_page(l_page_num)
        g_cards = Paginator(g_cards, 5).get_page(g_page_num)

        return render(request, 'card/card_all_page.html', {
            'l_cards': l_cards,
            'g_cards': g_cards,
        })


class LocalCardList(LoginRequiredMixin, views.View):

    def get(self, request):
        return render(request, 'card/local_list_page.html', {
            'cards': Card.objects.all(),
        })


class LocalCardRetrieve(LoginRequiredMixin, views.View):

    def get(self, request, pk):
        return render(request, 'card/local_retrieve_page.html', {
            'card': Card.objects.get(pk=pk),
        })


class LocalCardDetail(LoginRequiredMixin, views.View):

    def get(self, request, pk):
        card = Card.objects.get(pk=pk)
        if card.is_global:
            return redirect(reverse('card_local_retrieve'), {'pk': pk})

        # Get indexes from selected words and transport to context
        selected_indexes = [word.pk for word in card.words.all()]

        return render(request, 'card/local_retrieve_page.html', {
            'card': card,
            'words': Word.objects.filter(user=request.user),
            'selected_indexes': selected_indexes,
        })


class CardCreate(LoginRequiredMixin, views.View):

    def get(self, request):
        return render(request, 'card/card_create_page.html', {
            'form': CardForm,
        })

    def post(self, request):
        form = CardForm(request.POST)
        if form.is_valid():
            new_card: Card = form.save()

            new_card.created_by = request.user

            if 'words' in request.session:
                for word in request.session['words']:
                    new_card.words.add(Word.objects.get(pk=word))
                # Clear session
                del request.session['words']
                request.session.modified = True

            new_card.save()
            return redirect(reverse('cards'))
        # TODO: errors
        return redirect(reverse('home'))
