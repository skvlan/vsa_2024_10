from django.contrib.auth import get_user_model
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from api.permissions import IsSuperUser
from api.serializers import (CardSerializer, CardsSerializer, CarsSerializer,
                             ClientSerializer)
from carmarket.models import Car, Card


class ClientViewSet(ModelViewSet):
    permission_classes = [IsSuperUser]
    queryset = get_user_model().objects.all()
    serializer_class = ClientSerializer


class CardDetailView(RetrieveAPIView):
    permission_classes = [IsSuperUser]
    serializer_class = CardSerializer

    def get_object(self):

        return Card.objects.get(id=self.kwargs.get("pk"), order_number=self.kwargs.get("order"))


class CardsListView(ListAPIView):
    permission_classes = [AllowAny]
    queryset = Card.objects.all()
    serializer_class = CardsSerializer


class CarsListView(ListAPIView):
    permission_classes = [AllowAny]
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


class CardsCreateView(CreateAPIView):
    permission_classes = [IsSuperUser]
    queryset = Card.objects.all()
    serializer_class = CardSerializer


class CardsDeleteView(DestroyAPIView):
    permission_classes = [IsSuperUser]
    queryset = Card.objects.all()
    serializer_class = CardSerializer


class CardsUpdateView(UpdateAPIView):
    permission_classes = [IsSuperUser]
    queryset = Card.objects.all()
    serializer_class = CardSerializer
