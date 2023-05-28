from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from django.db.models import Q


class WordManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def get_word_status(self, id):
        '''
        Return status of word
        'n' - neutral
        'g' - good
        'b' - bad
        '''
        word_status = self.get(pk=id).ans_status
        if word_status > settings.STATUS_POINT:
            return 'g'
        elif word_status < -settings.STATUS_POINT:
            return 'b'
        return 'n'

    def get_filtered_objects(self, user, search=False):
        # Get all user's data
        # Objects - all words
        # Calculate all word's status
        if search:
            objects = self.filter(Q(user=user) &
                                  Q(original_word__istartswith=search))
        else:
            objects = self.filter(Q(user=user))
        good, bad, neutral = 0, 0, 0
        for object in objects:
            if object.ans_status > settings.STATUS_POINT:
                good += 1
            elif object.ans_status < -settings.STATUS_POINT:
                bad += 1
            else:
                neutral += 1
        return {
            'words': objects,
            'good': good,
            'bad': bad,
            'neutral': neutral,
        }


class Word(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    original_word = models.CharField('Original word', max_length=100)
    transcription = models.CharField(max_length=100, blank=True, null=True)
    translation = models.CharField(max_length=100)
    sentences = models.TextField('Sentences for describing word',
                                 max_length=500, blank=True, null=True)
    notes = models.TextField('Notes for additional information',
                             max_length=500, blank=True, null=True)
    ans_status = models.SmallIntegerField(
        'How many times user answer this right or wrong',
        validators=[MinValueValidator(-10), MaxValueValidator(10)],
        default=0,
        blank=True,
        editable=True,)
    objects = models.Manager()
    status_getter = WordManager()

    def list_sentences(self):
        return [s for s in self.sentences.split('\n')]

    def out_sentences(self):
        return '\n'.join(self.list_sentences())

    def save(self, *args, **kwargs):
        self.original_word = self.original_word.lower()
        self.transcription = self.transcription.lower() \
            if self.transcription \
            else self.transcription
        self.translation = self.translation.lower()
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("word_detail", kwargs={"pk": self.pk})

    def __str__(self):
        return f'''
    {self.user.username}# {self.original_word}\
    [{self.transcription}] - {self.translation}
    '''

    class Meta:
        ordering = ('original_word',)
