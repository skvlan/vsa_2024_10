from django.contrib.auth import get_user_model
from rest_framework.fields import CharField
from rest_framework.serializers import ModelSerializer

from carmarket.models import Car, Card


class ClientSerializer(ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["first_name", "last_name", "email", "is_staff"]


class CarSerializer(ModelSerializer):
    class Meta:
        model = Car
        fields = "__all__"


class CardSerializer(ModelSerializer):
    car = CarSerializer(read_only=True)

    class Meta:
        model = Card
        fields = ["user", "listing_date", "is_active", "contact_phone", "car"]


class CardsSerializer(ModelSerializer):
    car = CarSerializer(read_only=True)

    class Meta:
        model = Card
        fields = "__all__"


class CarsSerializer(ModelSerializer):
    category = CharField(source="get_category_display", read_only=True)
    fuel_type = CharField(source="get_fuel_type_display", read_only=True)
    transmission = CharField(source="get_transmission_display", read_only=True)

    class Meta:
        model = Car
        fields = "__all__"
