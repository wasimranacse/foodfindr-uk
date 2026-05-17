from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.analytics.models import RestaurantAnalyticsEvent
from apps.favourites.models import FavouriteRestaurant
from apps.locations.models import Area, City, Country
from apps.restaurants.models import Restaurant
from apps.reviews.models import Review
from apps.users.models import User


class RestaurantAPIPermissionTests(APITestCase):
    def setUp(self):
        self.country = Country.objects.create(name="United Kingdom", code="GB")
        self.city = City.objects.create(country=self.country, name="London", slug="london")
        self.area = Area.objects.create(
            city=self.city,
            name="Soho",
            slug="soho",
            postcode_prefix="W1",
            latitude=51.513000,
            longitude=-0.136500,
        )
        self.owner = User.objects.create_user(
            email="owner@example.com",
            password="StrongPass123!",
            full_name="Owner One",
            role=User.Role.RESTAURANT_OWNER,
            is_email_verified=True,
        )
        self.other_owner = User.objects.create_user(
            email="other-owner@example.com",
            password="StrongPass123!",
            full_name="Owner Two",
            role=User.Role.RESTAURANT_OWNER,
            is_email_verified=True,
        )
        self.customer = User.objects.create_user(
            email="customer@example.com",
            password="StrongPass123!",
            full_name="Customer One",
            role=User.Role.CUSTOMER,
            is_email_verified=True,
        )
        self.other_customer = User.objects.create_user(
            email="other-customer@example.com",
            password="StrongPass123!",
            full_name="Customer Two",
            role=User.Role.CUSTOMER,
            is_email_verified=True,
        )
        self.admin = User.objects.create_user(
            email="admin@example.com",
            password="StrongPass123!",
            full_name="Admin User",
            role=User.Role.ADMIN,
            is_email_verified=True,
        )
        self.approved = Restaurant.objects.create(
            owner=self.owner,
            name="Approved Bites",
            slug="approved-bites",
            country=self.country,
            city=self.city,
            area=self.area,
            postcode="W1D 3QF",
            latitude=51.513000,
            longitude=-0.136500,
            is_approved=True,
            is_open=True,
            average_rating=4.5,
            review_count=20,
            trust_score=85,
        )
        self.unapproved = Restaurant.objects.create(
            owner=self.owner,
            name="Draft Bites",
            slug="draft-bites",
            country=self.country,
            city=self.city,
            area=self.area,
            postcode="W1D 3QF",
            latitude=51.510000,
            longitude=-0.130000,
            is_approved=False,
            average_rating=5,
            review_count=1,
            trust_score=90,
        )
        self.other_restaurant = Restaurant.objects.create(
            owner=self.other_owner,
            name="Other Bites",
            slug="other-bites",
            country=self.country,
            city=self.city,
            area=self.area,
            postcode="W1D 3QF",
            latitude=51.520000,
            longitude=-0.150000,
            is_approved=True,
        )

    def test_public_only_sees_approved_restaurants(self):
        response = self.client.get(reverse("restaurant-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        names = {item["name"] for item in response.data["results"]}
        self.assertIn("Approved Bites", names)
        self.assertNotIn("Draft Bites", names)

    def test_owner_can_only_edit_own_restaurant(self):
        self.client.force_authenticate(self.owner)

        own_response = self.client.patch(
            reverse("owner-restaurant-update", kwargs={"pk": self.approved.id}),
            {"description": "Updated by owner"},
            format="json",
        )
        other_response = self.client.patch(
            reverse("owner-restaurant-update", kwargs={"pk": self.other_restaurant.id}),
            {"description": "Not allowed"},
            format="json",
        )

        self.assertEqual(own_response.status_code, status.HTTP_200_OK)
        self.assertEqual(other_response.status_code, status.HTTP_404_NOT_FOUND)

    def test_customer_can_only_edit_own_review_and_favourite(self):
        review = Review.objects.create(
            customer=self.customer,
            restaurant=self.approved,
            rating=4,
            is_approved=True,
        )
        other_review = Review.objects.create(
            customer=self.other_customer,
            restaurant=self.approved,
            rating=5,
            is_approved=True,
        )
        favourite = FavouriteRestaurant.objects.create(
            customer=self.customer,
            restaurant=self.approved,
        )
        other_favourite = FavouriteRestaurant.objects.create(
            customer=self.other_customer,
            restaurant=self.approved,
        )
        self.client.force_authenticate(self.customer)

        review_response = self.client.patch(
            reverse("customer-review-detail", kwargs={"pk": review.id}),
            {"comment": "Still good"},
            format="json",
        )
        other_review_response = self.client.patch(
            reverse("customer-review-detail", kwargs={"pk": other_review.id}),
            {"comment": "Nope"},
            format="json",
        )
        favourite_response = self.client.delete(
            reverse("customer-favourite-detail", kwargs={"pk": favourite.id})
        )
        other_favourite_response = self.client.delete(
            reverse("customer-favourite-detail", kwargs={"pk": other_favourite.id})
        )

        self.assertEqual(review_response.status_code, status.HTTP_200_OK)
        self.assertEqual(other_review_response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(favourite_response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(other_favourite_response.status_code, status.HTTP_404_NOT_FOUND)

    def test_admin_approval_works(self):
        self.client.force_authenticate(self.admin)

        response = self.client.post(
            reverse(
                "admin-restaurant-approval",
                kwargs={"pk": self.unapproved.id, "action": "approve"},
            ),
            {},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.unapproved.refresh_from_db()
        self.assertTrue(self.unapproved.is_approved)

    def test_nearby_search_returns_sorted_results(self):
        response = self.client.get(
            reverse("restaurant-nearby"),
            {"lat": "51.513000", "lng": "-0.136500", "radius": "5", "sort": "distance"},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data["results"]
        self.assertGreaterEqual(len(results), 2)
        self.assertEqual(results[0]["slug"], "approved-bites")
        self.assertLessEqual(results[0]["distance_km"], results[1]["distance_km"])


class AnalyticsAPITests(APITestCase):
    def test_event_can_be_recorded_for_approved_restaurant(self):
        owner = User.objects.create_user(
            email="owner2@example.com",
            password="StrongPass123!",
            full_name="Owner",
            role=User.Role.RESTAURANT_OWNER,
            is_email_verified=True,
        )
        restaurant = Restaurant.objects.create(
            owner=owner,
            name="Analytics Bites",
            slug="analytics-bites",
            is_approved=True,
        )

        response = self.client.post(
            reverse("analytics-event-create"),
            {"restaurant": restaurant.id, "event_type": "menu_view", "metadata": {"source": "test"}},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            RestaurantAnalyticsEvent.objects.filter(
                restaurant=restaurant,
                event_type="menu_view",
            ).exists()
        )
