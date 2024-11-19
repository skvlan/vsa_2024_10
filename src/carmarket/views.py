from django.shortcuts import render
from django.views.generic import DetailView

from .models import Car, Card


def cards_list_view(request):
    cards = Card.objects.filter(is_active=True).select_related("car")
    return render(request, "cards/cards_list.html", {"cards": cards})


class CardDetailView(DetailView):
    context_object_name = "car"
    model = Car
    template_name = "cards/card_detail.html"
