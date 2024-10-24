from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class CATEGORY_CHOISES(models.IntegerChoices):
    SEDAN = 0, "Sedan"
    HATCHBACK = 1, "Hatchback"
    UNIVERSAL = 2, "Universal"
    COUPE = 3, "Coupe"
    SUV = 4, "SUV"
    CROSSOVER = 5, "Crossover"
    MINIVAN = 6, "Minivan"
    PICKUP = 7, "Pickup"
    CABRIOLET = 8, "Cabriolet"


class FUEL_CHOISES(models.IntegerChoices):
    PETROL = 0, "Petrol"
    DIESEL = 1, "Diesel"
    ELECTRIC = 2, "Electric"
    HYBRID = 3, "Hybrid"


class TRANSMISSION_CHOISES(models.IntegerChoices):
    MANUAL = 0, "Manual"
    AUTOMATIC = 1, "Automatic"
    ROBOT = 2, "Robot"


class Car(models.Model):
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.IntegerField(max_length=4)
    generation = models.CharField(max_length=50)
    price = models.IntegerField(max_length=20)
    category = models.PositiveSmallIntegerField(choices=CATEGORY_CHOISES.choices, default=CATEGORY_CHOISES.UNIVERSAL)
    fuel_type = models.PositiveSmallIntegerField(choices=FUEL_CHOISES.choices, default=FUEL_CHOISES.PETROL)
    transmission = models.PositiveSmallIntegerField(
        choices=TRANSMISSION_CHOISES.choices, default=TRANSMISSION_CHOISES.MANUAL
    )
    description = models.TextField(max_length=1024, blank=True, null=True)
    favorites = models.ForeignKey("carmarket.Favorite", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="img/cars/", null=True, blank=True)

    def __str__(self):
        return f"{self.make} {self.model} ({self.pk})"


class Card(models.Model):
    car = models.OneToOneField("carmarket.Car", on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    listing_date = models.DateTimeField(_("date joined"), default=timezone.now)
    is_active = models.BooleanField(_("active"), default=True)
    views_count = models.PositiveIntegerField(default=0)
    contact_phone = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.car} {self.listing_date} {self.is_active} ({self.pk})"


class Favorite(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    cars = models.ManyToManyField("carmarket.Car", related_name="favorited_by")

    def __str__(self):
        return f"{self.user} ({self.pk})"


class ContactSeller(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    car = models.ForeignKey("carmarket.Car", on_delete=models.CASCADE, null=True, blank=True)
    message = models.TextField(max_length=1024, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "ContactSeller"
        verbose_name_plural = "ContactsSeller"

    def __str__(self):
        return f"Contact from {self.user} for {self.car} at {self.created_at}"


class SearchHistory(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Search by {self.user} at {self.created_at}"
