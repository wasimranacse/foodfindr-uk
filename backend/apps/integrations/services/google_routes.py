from django.conf import settings

from .base import IntegrationResult, not_configured


class GoogleRoutesClient:
    provider = "Google Routes API"

    def __init__(self, api_key: str | None = None):
        self.api_key = api_key if api_key is not None else getattr(settings, "GOOGLE_ROUTES_API_KEY", "")

    @property
    def is_configured(self) -> bool:
        return bool(self.api_key)

    def estimate_route(self, *, origin: dict, destination: dict) -> IntegrationResult:
        if not self.is_configured:
            return not_configured(self.provider)
        return IntegrationResult(
            configured=True,
            provider=self.provider,
            data={"origin": origin, "destination": destination},
            message="Google Routes placeholder ready for backend-only implementation.",
        )
