from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import (
    SignUpView,
    CheckToken,
    LoginView
)

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('email_confirmation/<uuid:token>/', CheckToken.as_view()),
]
