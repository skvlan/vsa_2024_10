from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions, routers

from api.views import (CardDetailView, CardsDeleteView, CardsListView,
                       CardsUpdateView, CarsCreateView, CarsDeleteView,
                       CarsListView, CarsUpdateView, ClientViewSet)

app_name = "api"

router = routers.DefaultRouter()
router.register("clients", ClientViewSet)


schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version="v1",
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("", include(router.urls)),
    path("docs/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    path("car/<int:pk>/cards/<int:order>/", CardDetailView.as_view(), name="card_details"),
    path("cards/", CardsListView.as_view(), name="cards_list"),
    path("cardы/create/", CardsDeleteView.as_view(), name="card_create"),
    path("cardы/<int:pk>/update/", CardsUpdateView.as_view(), name="card_update"),
    path("cardы/<int:pk>/delete/", CardsDeleteView.as_view(), name="card_delete"),
    path("cars/", CarsListView.as_view(), name="cars_list"),
    path("cars-create/", CarsCreateView.as_view(), name="cars_create"),
    path("cars/<int:pk>/delete/", CarsDeleteView.as_view(), name="cards-delete"),
    path("cars/<int:pk>/update/", CarsUpdateView.as_view(), name="cards-update"),
    path("auth/", include("djoser.urls.jwt")),
]
