from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from carmarket.models import Car


class TestCarMarketModels(TestCase):
    def setUp(self) -> None:
        self.client = Client()

        self.user_password = "testpassword"
        self.user = get_user_model().objects.create_user(email="user@example.com", password=self.user_password)

        self.manager_password = "adminpassword"
        self.manager = get_user_model().objects.create_superuser(
            email="admin@example.com", password=self.manager_password
        )

        self.car = Car.objects.create(
            make="Toyota",
            model="Camry",
            year=2020,
            generation="XV70",
            price=30000,
            category=0,
            fuel_type=0,
            transmission=1,
            description="A reliable car.",
        )

    def test_user_login_wrong_email(self):
        user_login = self.client.login(email="wrong_email", password=self.user_password)
        self.assertFalse(user_login)

    def test_user_login_wrong_password(self):
        user_login = self.client.login(email=self.user.email, password="wrong_password")
        self.assertFalse(user_login)

    def test_manager_access_admin_panel(self):
        self.client.force_login(self.manager)
        response = self.client.get(reverse("admin:index"))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_create_car(self):
        car_count = Car.objects.count()
        new_car = Car.objects.create(
            make="Honda",
            model="Accord",
            year=2021,
            generation="10th",
            price=25000,
            category=0,
            fuel_type=0,
            transmission=1,
            description="Another reliable car.",
        )
        self.assertEqual(Car.objects.count(), car_count + 1)
        self.assertEqual(new_car.model, "Accord")
