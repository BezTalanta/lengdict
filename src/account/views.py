from django.shortcuts import (
    render,
    redirect,
    get_object_or_404,
)
from django.urls import reverse
from django.contrib.auth import (
    get_user_model,
    authenticate,
    login
)
from django.contrib.messages import info
from django.conf import settings
from django.views import View
from django.core.mail import send_mail

from .forms import UserForm
from .models import UserEmailConfirmation


class SignUpView(View):
    '''
    Simple low level register view
    '''

    def get(self, request):
        return render(request, 'account/signup_page.html', {
            'form': UserForm,
        })

    def post(self, request):
        user = UserForm(request.POST)
        if user.is_valid():
            created_user = get_user_model().objects.create_user(
                email=user.cleaned_data['email'],
                username=user.cleaned_data['username'],
                password=user.cleaned_data['pass1'],
            )
            email_confirmation = UserEmailConfirmation.objects.create(
                user=created_user,
            )
            _ = send_mail(
                'Email confirmation',
                f'You have tried to register account on \
{settings.EMAIL_SITE_NAME}. To confirm that operation please go to the link \
{settings.EMAIL_SITE_NAME}/account/email_confirmation/{email_confirmation.token}',
                settings.EMAIL_HOST_USER,
                [created_user.email],
                True,
            )
            info(request, 'Confirm your email then login')
            return redirect(reverse('home'))
        return render(request, 'account/signup_page.html', {
            'form': user,
        })


class LoginView(View):
    '''
    Simple low level login view
    '''

    def get(self, request):
        if not request.user.is_anonymous:
            return redirect(reverse('home'))
        return render(request, 'account/login_page.html')

    def post(self, request):
        user = authenticate(request,
                            username=request.POST['username'],
                            password=request.POST['password'])

        if not user:
            info(request, 'Wrong username or password')
            return redirect(reverse('login'))
        if user.is_email_confirmed:
            login(request, user)
            return redirect(reverse('home'))
        info(request, 'Check your mailbox')
        return render(request, 'account/login_page.html')


class CheckToken(View):

    def get(self, request, token):
        email_confirm_get = get_object_or_404(UserEmailConfirmation,
                                              token=token)
        email_confirm_get.user.is_email_confirmed = True
        email_confirm_get.user.save()
        info(request, 'You successfully confirmed your email, now you can login')
        return redirect(reverse('home'))
