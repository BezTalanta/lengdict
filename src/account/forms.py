from django import forms
from django.contrib.auth import get_user_model
from django.db.models import Q


class UserForm(forms.Form):
    email = forms.EmailField(max_length=255)
    username = forms.CharField(max_length=255)
    pass1 = forms.CharField(max_length=255, widget=forms.PasswordInput)
    pass2 = forms.CharField(max_length=255, widget=forms.PasswordInput)

    def is_valid(self):
        valid = super().is_valid()
        if not valid:
            return False
        if self.cleaned_data['pass1'] != self.cleaned_data['pass2']:
            self.errors['pass1'] = ['Passwords are different']
            return False
        if get_user_model().objects.filter(
            Q(username=self.cleaned_data['username']) |
            Q(email=self.cleaned_data['email'])).exists():
            self.errors['email'] = ['Username or email already exist']
            return False
        return True
