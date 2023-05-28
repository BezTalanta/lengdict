from django.urls import path
from .views import (
    DictView,
    SelectDictView,
    AddWordView,
    WordDetail,
    DeleteConfirm,
)


urlpatterns = [
    path('', DictView.as_view(), name='dict'),
    path('select/', SelectDictView.as_view(), name='select'),
    path('add/', AddWordView.as_view(), name='word_add'),
    path('word/<int:pk>/', WordDetail.as_view(), name='word_detail'),
    path('sure/<int:pk>/', DeleteConfirm.as_view(), name='word_delete'),

    # path('run/', RunView.as_view(), name='run'),
    # path('run/menu/', RunView.as_view(), name='run'),
]
