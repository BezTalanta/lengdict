from django.contrib import admin

from .models import Word


class WordAdmin(admin.ModelAdmin):
    list_display = ('user', 'original_word', 'ans_status')
    # list_editable = ('ans_status',)
    ordering = ('user', 'original_word')


admin.site.register(Word, WordAdmin)
