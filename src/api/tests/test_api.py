import unittest
from sre_constants import ANY

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.exceptions import ErrorDetail
from rest_framework.status import (HTTP_200_OK, HTTP_201_CREATED,
                                   HTTP_204_NO_CONTENT, HTTP_401_UNAUTHORIZED,
                                   HTTP_403_FORBIDDEN)
from rest_framework.test import APIClient

from carmarket.utils.samples import sample_car, sample_card


class TestApi(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model()(email="user@example.com")
        self.user.set_password("qwerty1234")
        self.user.save()

        self.car = sample_car(
            make="Toyota",
            model="Camry",
            year=2020,
            generation="XV70",
            category=0,
            fuel_type=0,
            transmission=1,
        )
        self.card = sample_card(
            user=self.user,
            car=self.car,
            title="Test Card",
            order_number=1,
            is_active=True,
            contact_phone="+1234567890",
        )

    def test_card_details_no_access(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get(
            reverse("api:card_details", kwargs={"pk": self.card.pk, "order": self.card.order_number}),
        )

        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

        self.assertEqual(
            response.data,
            {
                "detail": ErrorDetail(
                    string="You do not have permission to perform this action.", code="permission_denied"
                ),
            },
        )

    def test_card_details_access(self):
        self.user.is_superuser = True
        self.user.save()
        self.client.force_authenticate(user=self.user)

        response = self.client.get(
            reverse("api:card_details", kwargs={"pk": self.card.pk, "order": self.card.order_number}),
        )

        self.assertEqual(response.data, HTTP_200_OK)
        self.assertEqual(
            response.data,
            {
                "id": ANY,
                "order_number": 1,
                "user": self.user.id,
                "title": "Test Card",
                "is_active": True,
                "contact_phone": "+1234567890",
                "car": {
                    "make": "Toyota",
                    "model": "Camry",
                    "year": 2020,
                    "generation": "XV70",
                    "category": 0,
                    "fuel_type": 0,
                    "transmission": 1,
                },
            },
        )
        self.assertEqual(response.data["title"], "Test Card")

    @unittest.expectedFailure
    def test_card_list_no_access(self):
        response = self.client.get(reverse("api:cards_list"))
        self.assertEqual(response.data, HTTP_401_UNAUTHORIZED)

    def test_card_list(self):
        response = self.client.get(reverse("api:cards_list"))
        self.assertEqual(response.data, HTTP_200_OK)
        self.assertEqual(response.data, {"id": ANY, "title": "Test Card", "is_active": True})

    def test_card_create(self):
        self.user.is_superuser = True
        self.user.save()
        self.client.force_authenticate(user=self.user)
        data = {
            "title": "New Test Card",
            "order_number": 2,
            "is_active": True,
            "contact_phone": "+0987654321",
            "car": {
                "make": "Honda",
                "model": "Civic",
                "year": 2021,
                "generation": "XI",
                "category": 1,
                "fuel_type": 1,
                "transmission": 0,
            },
        }

        response = self.client.post(reverse("api:card_create"), data, format="json")

        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertEqual(
            response.data,
            {
                "id": ANY,
                "title": "New Test Card",
                "order_number": 2,
                "is_active": True,
                "contact_phone": "+0987654321",
                "user": self.user.id,
                "car": {
                    "make": "Honda",
                    "model": "Civic",
                    "year": 2021,
                    "generation": "XI",
                    "category": 1,
                    "fuel_type": 1,
                    "transmission": 0,
                },
            },
        )

    def test_card_update(self):
        self.user.is_superuser = True
        self.user.save()
        self.client.force_authenticate(user=self.user)

        update_data = {
            "title": "Updated Test Card",
            "is_active": False,
            "contact_phone": "+1122334455",
        }

        response = self.client.patch(
            reverse("api:card_update", kwargs={"pk": self.card.pk}), update_data, format="json"
        )

        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(
            response.data,
            {
                "id": self.card.pk,
                "title": "Updated Test Card",
                "order_number": self.card.order_number,
                "is_active": False,
                "contact_phone": "+1122334455",
                "user": self.user.id,
                "car": {
                    "make": "Toyota",
                    "model": "Camry",
                    "year": 2020,
                    "generation": "XV70",
                    "category": 0,
                    "fuel_type": 0,
                    "transmission": 1,
                },
            },
        )

    def test_card_delete(self):
        self.user.is_superuser = True
        self.user.save()
        self.client.force_authenticate(user=self.user)

        response = self.client.delete(reverse("api:card_delete", kwargs={"pk": self.card.pk}))

        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)

        response = self.client.get(
            reverse("api:card_details", kwargs={"pk": self.card.pk, "order": self.card.order_number})
        )
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data,
            {
                "detail": ErrorDetail(
                    string="You do not have permission to perform this action.", code="permission_denied"
                ),
            },
        )
