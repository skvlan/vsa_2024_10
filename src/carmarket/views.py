from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Car, Card


class CardsListView(ListView):
    context_object_name = "cards"
    model = Card
    template_name = "cards/cards_list.html"

    def get_queryset(self):
        return Card.objects.filter(is_active=True).select_related("car")


class CardDetailView(DetailView):
    context_object_name = "car"
    model = Car
    template_name = "cards/card_detail.html"
