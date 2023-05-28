from django.contrib import admin
from .models import MUser, UserEmailConfirmation


class MUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email',
                    'is_email_confirmed', 'is_user_premium',
                    'is_superuser']
    list_filter = ['is_email_confirmed', 'is_user_premium',
                   'is_superuser', 'is_staff']
    list_editable = ['is_email_confirmed', 'is_user_premium']


class EmailConfirmationAdmin(admin.ModelAdmin):
    list_display = ['user', 'token']
    readonly_fields = ['user', 'token']


admin.site.register(MUser, MUserAdmin)
admin.site.register(UserEmailConfirmation, EmailConfirmationAdmin)
