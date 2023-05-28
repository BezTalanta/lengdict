from django.urls import path
from .views import (
    RunView,
    ResultView,
    MenuView,
)

urlpatterns = [
    path('', RunView.as_view(), name='run'),
    path('menu/', MenuView.as_view(), name='run_menu'),
    path('result/', ResultView.as_view(), name='run_result')
]
