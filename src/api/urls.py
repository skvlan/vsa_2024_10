from django.urls import include, path
from rest_framework import routers

from api.views import CardDetailView, ClientViewSet

app_name = "api"

router = routers.DefaultRouter()
router.register("clients", ClientViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("car/<int:pk>/cards/<int:order>/", CardDetailView.as_view(), name="card_details"),
]
