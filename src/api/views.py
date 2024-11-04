from django.contrib.auth import get_user_model
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import ModelSerializer
from rest_framework.viewsets import ModelViewSet

from api.serializers import (CardSerializer, CardsSerializer, CarsSerializer,
                             ClientSerializer)
from carmarket.models import Car, Card


class ClientViewSet(ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = ClientSerializer


class CardDetailView(RetrieveAPIView):
    serializer_class = CardSerializer

    def get_object(self):

        return Card.objects.get(id=self.kwargs.get("pk"), order_number=self.kwargs.get("order"))


class CardsListView(ListAPIView):
    queryset = Card.objects.all()
    serializer_class = CardsSerializer


class CarsListView(ListAPIView):
    queryset = Car.objects.all()
    serializer_class = CarsSerializer


class CarsCreateView(CreateAPIView):
    queryset = Car.objects.all()
    serializer_class = CarsSerializer


class CarsDeleteView(DestroyAPIView):
    queryset = Car.objects.all()
    serializer_class = CarsSerializer


class CarsUpdateView(UpdateAPIView):
    queryset = Car.objects.all()
    serializer_class = CarsSerializer
