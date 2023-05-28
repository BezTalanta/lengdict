from django.contrib.auth import get_user_model

from word.models import Word


gm = get_user_model()

Word.objects.create(
    user=gm.objects.first(),
    original_word='apple2',
    transcription='dsa',
    translation='dsadsa'
)
