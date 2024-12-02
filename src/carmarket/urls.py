from django.conf.urls.static import static
from django.urls import path

from carmarket.views import (AddToFavorites, CardDetailView, CardsListView,
                             CreateCard, DeleteCard, FavoritesListView,
                             GenerateCardsView, GenerateCarsView,
                             GenerateContactsView, GenerateFavoritesView,
                             RemoveFromFavorites, UpdateCard)
from config.settings import dev

app_name = "cards"
urlpatterns = [
    path("cards/", CardsListView.as_view(), name="cards_list"),
    path("cards/<int:pk>/", CardDetailView.as_view(), name="card_detail"),
    path("create-card/", CreateCard.as_view(), name="card_create"),
    path("update-card/<int:pk>/", UpdateCard.as_view(), name="card_update"),
    path("delete-card/<int:pk>/", DeleteCard.as_view(), name="card_delete"),
    path("favorites/<int:pk>/", AddToFavorites.as_view(), name="add_to_favorites"),
    path("remove_from_favorites/<int:pk>/", RemoveFromFavorites.as_view(), name="remove_from_favorites"),
    path("favorites/", FavoritesListView.as_view(), name="favorites_list"),
    path("generate-cars/", GenerateCarsView.as_view(), name="generate_cars"),
    path("generate-cards/", GenerateCardsView.as_view(), name="generate_cards"),
    path("generate-favorites/", GenerateFavoritesView.as_view(), name="generate_favorites"),
    path("generate-contacts/", GenerateContactsView.as_view(), name="generate_contacts"),
]

if dev.DEBUG:
    urlpatterns += static(dev.MEDIA_URL, document_root=dev.MEDIA_ROOT)
