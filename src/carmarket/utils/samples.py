from carmarket.models import Car, Card


def sample_card(user, car: Car, title: str, **params) -> Card:
    default = {
        "order_number": 1,
        "contact_phone": "+1234567890",
        "is_active": True,
    }
    default.update(params)
    return Card.objects.create(user=user, car=car, title=title, **default)


def sample_car(**params) -> Car:
    default = {
        "make": "Toyota",
        "model": "Camry",
        "year": 2020,
        "generation": "XV70",
        "price": 30000,
        "category": 0,
        "fuel_type": 0,
        "transmission": 1,
        "description": "Another reliable car.",
    }
    default.update(params)
    return Car.objects.create(**default)
