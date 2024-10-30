from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from carmarket.models import Car
from carmarket.utils.samples import sample_car, sample_card


class TestCarMarketModels(TestCase):
    def setUp(self) -> None:
        self.client = Client()

        self.user_password = "testpassword"
        self.user = get_user_model().objects.create_user(email="user@example.com", password=self.user_password)

        self.manager_password = "adminpassword"
        self.manager = get_user_model().objects.create_superuser(
            email="admin@example.com", password=self.manager_password
        )

        self.car = sample_car(carmarket=sample_card(title="Test Card"), order_number=1)

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
        new_car = sample_car(carmarket=sample_card(title="New Test Card"), order_number=1)
        self.assertEqual(Car.objects.count(), car_count + 1)
        self.assertEqual(new_car.model, "Camry")
