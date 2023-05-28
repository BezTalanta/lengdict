from django import forms

from .models import Word


class WordForm(forms.ModelForm):

    class Meta:
        model = Word
        fields = ('original_word', 'transcription',
                  'translation', 'sentences', 'notes')
