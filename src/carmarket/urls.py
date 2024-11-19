from django.urls import path

from . import views
from .views import CardDetailView

urlpatterns = [
    path("cards/", views.cards_list_view, name="cards_list"),
    path("cards/<int:pk>/", CardDetailView.as_view(), name="card_detail"),
]
