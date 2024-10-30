from carmarket.models import Car, Card


def sample_card(title: str, **params) -> Card:
    default = {"description": "Some text"}
    default.update(params)
    return Card.objects.create(title=title, **default)


def sample_car(carmarket: Card, order_number: int, **params) -> Card:
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
    return Car.objects.create(carmarket=carmarket, order_number=order_number, **default)
