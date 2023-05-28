from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model

from word.models import Word


def generic_path(instance, filename):
    return f'{instance.user.id}/{filename}'


class Card(models.Model):
    '''
        Card model, can contain some words, description and something else
    '''

    title = models.CharField('Title of card', max_length=100)
    description = models.CharField('Description of card', max_length=100,
                                   blank=True, default='')
    words = models.ManyToManyField(Word, related_name='cards')
    created_by = models.ForeignKey(get_user_model(),
                                   on_delete=models.CASCADE,
                                   verbose_name='Who has created this card',
                                   blank=True, null=True)
    image_link = models.ImageField("Card's image",
                                   upload_to=generic_path,
                                   default='media/not_found.png')
    is_global = models.BooleanField('Is this card global', default=False)

    def get_absolute_url(self):
        return reverse("card_local_retrieve", kwargs={"pk": self.pk})

    def __str__(self):
        return self.description

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Card'
        verbose_name_plural = 'Cards'
        ordering = ('title',)


# class GlobalCard(models.Model):
#     '''
#         Some attributes are required for global card
#     '''
#     card = models.ForeignKey(Card, on_delete=)
