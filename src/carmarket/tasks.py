import time

from celery import shared_task
from django.contrib.auth import get_user_model
from faker import Faker
from faker.generator import random
from faker_vehicle import VehicleProvider

from carmarket.models import Car, Card, ContactSeller, Favorite

fake = Faker()
fake.add_provider(VehicleProvider)


@shared_task
def mine_bitcoin():
    time.sleep(random.randint(1, 10))


@shared_task
def normalize_email_task(filter):
    all_users = get_user_model().objects.filter(**filter)

    if all_users:
        for user in all_users:
            print(f"Working with {user.email}")
            user.save()
    else:
        print("Empty data")

    return f"Checked {len(all_users)} users"


@shared_task
def generate_cars(count=10):
    categories = [choice[0] for choice in Car.CATEGORY_CHOISES.choices]
    fuel = [choice[0] for choice in Car.FUEL_CHOISES.choices]
    transmissions = [choice[0] for choice in Car.TRANSMISSION_CHOISES.choices]

    for _ in range(count):
        vehicle = fake.vehicle_object()
        car = Car.objects.create(
            make=vehicle["Make"],
            model=vehicle["Model"],
            year=int(vehicle["Year"]),
            generation=f"Gen-{random.randint(1, 10)}",
            price=random.randint(1000, 50000),
            mileage=random.randint(0, 350000),
            category=random.choice(categories),
            fuel_type=random.choice(fuel),
            transmission=random.choice(transmissions),
            description=fake.text(max_nb_chars=100),
        )
        print(f"Generated Car: {car}")


@shared_task
def generate_cards(count=10, user_id=None):
    User = get_user_model()

    if not user_id:
        user = User.objects.first()
    else:
        user = User.objects.filter(id=user_id).first()

    if not user:
        raise ValueError("No valid user found to assign cards.")

    available_cars = Car.objects.filter(card__isnull=True)

    if available_cars.count() < count:
        raise ValueError(
            f"Not enough cars available to create {count} cards. Only {available_cars.count()} cars available."
        )

    for car in random.sample(list(available_cars), count):
        card = Card.objects.create(
            title=fake.sentence(nb_words=3),
            car=car,
            user=user,
            listing_date=fake.date_time_this_year(),
            is_active=True,
            views_count=random.randint(0, 1000),
            order_number=random.randint(1, Car.CARD_MAX_COUNT),
            contact_phone=fake.phone_number(),
        )
        print(f"Generated Card: {card.title} for Car {car.make} {car.model}")


@shared_task
def generate_favorites(count=10):
    users = get_user_model().objects.all()
    cars = Car.objects.all()

    if not users.exists() or not cars.exists():
        print("No users or cars to associate with favorites.")
        return

    for _ in range(count):
        user = random.choice(users)
        favorite, _ = Favorite.objects.get_or_create(user=user)
        random_cars = random.sample(list(cars), min(len(cars), random.randint(1, 5)))
        favorite.cars.add(*random_cars)
        print(f"Generated Favorites for {user}: {favorite.cars.all()}")


@shared_task
def generate_contacts(count=10):
    users = get_user_model().objects.all()
    cars = Car.objects.all()

    if not users.exists() or not cars.exists():
        print("No users or cars to associate with contacts.")
        return

    for _ in range(count):
        user = random.choice(users)
        car = random.choice(cars)
        contact = ContactSeller.objects.create(
            user=user,
            car=car,
            message=fake.text(max_nb_chars=100),
        )
        print(f"Generated Contact: {contact}")
