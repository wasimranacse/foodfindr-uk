from django.conf import settings

from .base import IntegrationResult, not_configured


class GooglePlacesClient:
    provider = "Google Places API"

    def __init__(self, api_key: str | None = None):
        self.api_key = api_key if api_key is not None else getattr(settings, "GOOGLE_PLACES_API_KEY", "")

    @property
    def is_configured(self) -> bool:
        return bool(self.api_key)

    def find_place(self, *, query: str, latitude=None, longitude=None) -> IntegrationResult:
        if not self.is_configured:
            return not_configured(self.provider)
        return IntegrationResult(
            configured=True,
            provider=self.provider,
            data={"query": query, "latitude": latitude, "longitude": longitude},
            message="Google Places placeholder ready for backend-only implementation.",
        )
