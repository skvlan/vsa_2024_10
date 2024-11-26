from django import forms

from .models import Car, Card


class CardCarForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = ["title", "contact_phone", "order_number", "is_active"]

    car_make = forms.CharField(max_length=50, label="Make")
    car_model = forms.CharField(max_length=50, label="Model")
    car_year = forms.IntegerField(label="Year")
    car_generation = forms.CharField(max_length=50, label="Generation")
    car_price = forms.IntegerField(label="Price")
    car_mileage = forms.IntegerField(label="Mileage", initial=0)
    car_category = forms.ChoiceField(choices=Car.CATEGORY_CHOISES.choices, label="Category")
    car_fuel_type = forms.ChoiceField(choices=Car.FUEL_CHOISES.choices, label="Fuel Type")
    car_transmission = forms.ChoiceField(choices=Car.TRANSMISSION_CHOISES.choices, label="Transmission")
    car_description = forms.CharField(max_length=1024, widget=forms.Textarea, required=False, label="Description")
    car_image = forms.ImageField(required=False, label="Image")

    def __init__(self, *args, **kwargs):
        card_instance = kwargs.get("instance")
        if card_instance:
            car_instance = card_instance.car
            kwargs["initial"] = {
                "car_make": car_instance.make,
                "car_model": car_instance.model,
                "car_year": car_instance.year,
                "car_generation": car_instance.generation,
                "car_price": car_instance.price,
                "car_mileage": car_instance.mileage,
                "car_category": car_instance.category,
                "car_fuel_type": car_instance.fuel_type,
                "car_transmission": car_instance.transmission,
                "car_description": car_instance.description,
                "car_image": car_instance.image,
            }
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        card = super().save(commit=False)

        car = getattr(card, "car", None)
        if car is None:
            car = Car()

        car.make = self.cleaned_data["car_make"]
        car.model = self.cleaned_data["car_model"]
        car.year = self.cleaned_data["car_year"]
        car.generation = self.cleaned_data["car_generation"]
        car.price = self.cleaned_data["car_price"]
        car.mileage = self.cleaned_data["car_mileage"]
        car.category = self.cleaned_data["car_category"]
        car.fuel_type = self.cleaned_data["car_fuel_type"]
        car.transmission = self.cleaned_data["car_transmission"]
        car.description = self.cleaned_data["car_description"]
        car.image = self.cleaned_data["car_image"]

        if commit:
            car.save()
            card.car = car
            card.save()

        return card
