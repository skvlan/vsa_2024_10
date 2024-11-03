from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer

from carmarket.models import Card


class ClientSerializer(ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["first_name", "last_name", "email", "is_staff"]


class CardSerializer(ModelSerializer):
    class Meta:
        model = Card
        fields = ["id", "car", "listing_date", "is_active", "contact_phone"]
