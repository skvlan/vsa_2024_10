from django.urls import path

from . import views
from .views import CardDetailView, CardsListView

urlpatterns = [
    path("cards/", CardsListView.as_view(), name="cards_list"),
    path("cards/<int:pk>/", CardDetailView.as_view(), name="card_detail"),
]
