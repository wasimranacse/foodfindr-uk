from django.test import SimpleTestCase, override_settings

from apps.integrations.services.deliveroo_signature import DeliverooSignatureClient
from apps.integrations.services.external_ordering import validate_external_order_url
from apps.integrations.services.food_standards_agency import FoodHygieneRatingClient
from apps.integrations.services.google_places import GooglePlacesClient
from apps.integrations.services.google_routes import GoogleRoutesClient
from apps.integrations.services.just_eat_partner import JustEatPartnerClient
from apps.integrations.services.uber_direct import UberDirectClient


@override_settings(
    GOOGLE_PLACES_API_KEY="",
    GOOGLE_ROUTES_API_KEY="",
    FSA_API_BASE_URL="",
    UBER_DIRECT_API_KEY="",
    DELIVEROO_API_KEY="",
    JUST_EAT_API_KEY="",
)
class IntegrationPlaceholderTests(SimpleTestCase):
    def test_clients_are_safe_without_external_api_keys(self):
        results = [
            FoodHygieneRatingClient().lookup_business(postcode="SW1A 1AA"),
            GooglePlacesClient().find_place(query="FoodFindr"),
            GoogleRoutesClient().estimate_route(origin={}, destination={}),
            UberDirectClient().create_delivery_quote(),
            DeliverooSignatureClient().create_delivery_quote(),
            JustEatPartnerClient().get_restaurant_status(),
        ]

        self.assertTrue(all(result.configured is False for result in results))
        self.assertTrue(all(result.data == {} for result in results))

    def test_external_ordering_url_validation_is_provider_scoped(self):
        self.assertTrue(
            validate_external_order_url("uber_eats", "https://www.ubereats.com/store/example")
        )
        self.assertTrue(
            validate_external_order_url("deliveroo", "https://deliveroo.co.uk/menu/example")
        )
        self.assertTrue(
            validate_external_order_url("just_eat", "https://www.just-eat.co.uk/restaurants/example")
        )
        self.assertTrue(
            validate_external_order_url("direct", "https://restaurant.example/order")
        )
        self.assertFalse(
            validate_external_order_url("uber_eats", "https://example.com/not-uber")
        )
