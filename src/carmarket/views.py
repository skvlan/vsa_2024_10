from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from .forms import CardCarForm, CarSearchForm
from .models import Car, Card, Favorite
from .tasks import (generate_cards, generate_cars, generate_contacts,
                    generate_favorites)


class CardsListView(ListView):
    context_object_name = "cards"
    model = Card
    template_name = "cards/cards_list.html"
    cards = Card.objects.all()

    form_class = CarSearchForm

    def get_queryset(self):
        queryset = Card.objects.filter(is_active=True).select_related("car")
        form = self.form_class(self.request.GET)

        if form.is_valid():
            make = form.cleaned_data.get("make")
            model = form.cleaned_data.get("model")
            year_min = form.cleaned_data.get("year_min")
            year_max = form.cleaned_data.get("year_max")
            category = form.cleaned_data.get("category")
            fuel_type = form.cleaned_data.get("fuel_type")
            transmission = form.cleaned_data.get("transmission")

            if make:
                queryset = queryset.filter(car__make__icontains=make)
            if model:
                queryset = queryset.filter(car__model__icontains=model)
            if year_min:
                queryset = queryset.filter(car__year__gte=year_min)
            if year_max:
                queryset = queryset.filter(car__year__lte=year_max)
            if category:
                queryset = queryset.filter(car__category=category)
            if fuel_type:
                queryset = queryset.filter(car__fuel_type=fuel_type)
            if transmission:
                queryset = queryset.filter(car__transmission=transmission)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = self.form_class(self.request.GET)
        return context


class CardDetailView(DetailView):
    context_object_name = "car"
    model = Car
    template_name = "cards/card_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


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

        return redirect("cards:favorites_list")


class RemoveFromFavorites(LoginRequiredMixin, View):
    def post(self, request, pk):
        car = get_object_or_404(Car, pk=pk)
        favorite = Favorite.objects.filter(user=request.user).first()

        if favorite and car in favorite.cars.all():
            favorite.cars.remove(car)
            messages.success(request, f"{car.make} {car.model} has been removed from your favorites.")

        return redirect("cards:favorites_list")


class FavoritesListView(LoginRequiredMixin, ListView):
    model = Car
    template_name = "favorites/favorites_list.html"
    context_object_name = "favorites"

    def get_queryset(self):
        favorite = Favorite.objects.filter(user=self.request.user).first()
        if self.request.user.is_authenticated:
            favorite = Favorite.objects.filter(user=self.request.user).first()
            if favorite:
                return favorite.cars.all()
        messages.info(self.request, "You need to log in to view your favorites.")
        return []

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("login")
        return super().dispatch(request, *args, **kwargs)


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
