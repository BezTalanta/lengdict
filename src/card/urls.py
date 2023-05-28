from django.urls import path
from .views import (
    CardListAll,
    CardCreate,
    LocalCardList,
    LocalCardRetrieve,
    LocalCardDetail,
)

urlpatterns = [
    path('', CardListAll.as_view(), name='cards'),
    path('create/', CardCreate.as_view(), name='create_card'),
    path('local/', LocalCardList.as_view(), name='card_local_list'),
    path('local/<int:pk>/',
         LocalCardRetrieve.as_view(),
         name='card_local_retrieve'),
    path('local/detail/<int:pk>/',
         LocalCardDetail.as_view(),
         name='card_local_detail'),
]
