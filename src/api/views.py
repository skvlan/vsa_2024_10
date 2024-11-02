from django.contrib.auth import get_user_model
from rest_framework.generics import RetrieveAPIView
from rest_framework.serializers import ModelSerializer
from rest_framework.viewsets import ModelViewSet

from api.serializers import CardSerializer, ClientSerializer
from carmarket.models import Card


class ClientViewSet(ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = ClientSerializer


class CardDetailView(RetrieveAPIView):
    serializer_class = CardSerializer

    def get_object(self):
        print(self.kwargs)

        return Card.objects.get(card_id=self.kwargs.get("pk"), order_number=self.kwargs.get("order"))
