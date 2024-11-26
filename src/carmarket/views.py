from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from .forms import CardCarForm
from .models import Car, Card, Favorite
from .tasks import (generate_cards, generate_cars, generate_contacts,
                    generate_favorites, mine_bitcoin, normalize_email_task)


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


class CreateCard(LoginRequiredMixin, CreateView):
    template_name = "cards/card_create.html"
    form_class = CardCarForm
    model = Card
    success_url = reverse_lazy("cards:cards_list")

    def form_valid(self, form):
        card = form.save(commit=False)

        car = Car(
            make=form.cleaned_data["car_make"],
            model=form.cleaned_data["car_model"],
            year=form.cleaned_data["car_year"],
            generation=form.cleaned_data["car_generation"],
            price=form.cleaned_data["car_price"],
            mileage=form.cleaned_data["car_mileage"],
            category=form.cleaned_data["car_category"],
            fuel_type=form.cleaned_data["car_fuel_type"],
            transmission=form.cleaned_data["car_transmission"],
            description=form.cleaned_data["car_description"],
            image=form.cleaned_data["car_image"],
        )
        car.save()

        card.car = car
        card.user = self.request.user
        card.save()

        return super().form_valid(form)


class UpdateCard(LoginRequiredMixin, UpdateView):
    model = Card
    template_name = "cards/card_update.html"
    form_class = CardCarForm
    success_url = reverse_lazy("cards:cards_list")

    def get_queryset(self):
        return Card.objects.filter(user=self.request.user)

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class DeleteCard(LoginRequiredMixin, DeleteView):
    model = Card
    template_name = "cards/card_delete.html"
    success_url = reverse_lazy("cards:cards_list")

    def get_queryset(self):
        return Card.objects.filter(user=self.request.user)


class AddToFavorites(LoginRequiredMixin, View):

    def post(self, request, pk):
        car = get_object_or_404(Car, pk=pk)

        favorite, created = Favorite.objects.get_or_create(user=request.user)

        if car not in favorite.cars.all():
            favorite.cars.add(car)

        return redirect("cards:card_detail", pk=car.pk)


class FavoritesListView(LoginRequiredMixin, ListView):
    model = Car
    template_name = "favorites/favorites_list.html"
    context_object_name = "favorites"

    def get_queryset(self):
        favorite = Favorite.objects.filter(user=self.request.user).first()
        if favorite:
            return favorite.cars.all()
        return []


def bitcoin(request: HttpRequest) -> HttpResponse:
    mine_bitcoin.delay()
    return HttpResponse("Task is started!")


def normalize_emails(request: HttpRequest) -> HttpResponse:
    normalize_email_task.delay(filter={"email__endswith": ".com"})
    return HttpResponse("Task is started!")


class GenerateCarsView(View):
    def get(self, request, *args, **kwargs):
        count = request.GET.get("count", 10)
        generate_cars.delay(count=int(count))
        return HttpResponse("Car generation started.")


class GenerateCardsView(View):
    def get(self, request, *args, **kwargs):
        generate_cards.delay(count=kwargs.get("count", 10))
        return HttpResponse("Card generation started.")


class GenerateFavoritesView(View):
    def get(self, request, *args, **kwargs):
        generate_favorites.delay(count=kwargs.get("count", 10))
        return HttpResponse("Favorite generation started.")


class GenerateContactsView(View):
    def get(self, request, *args, **kwargs):
        generate_contacts.delay(count=kwargs.get("count", 10))
        return HttpResponse("Contact generation started.")
