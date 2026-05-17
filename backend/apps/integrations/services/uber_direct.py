from django.conf import settings

from .base import IntegrationResult, not_configured


class UberDirectClient:
    provider = "Uber Direct"

    def __init__(self, api_key: str | None = None):
        self.api_key = api_key if api_key is not None else getattr(settings, "UBER_DIRECT_API_KEY", "")

    @property
    def is_configured(self) -> bool:
        return bool(self.api_key)

    def create_delivery_quote(self, **payload) -> IntegrationResult:
        if not self.is_configured:
            return not_configured(self.provider)
        return IntegrationResult(
            configured=True,
            provider=self.provider,
            data=payload,
            message="Uber Direct placeholder ready for backend-only implementation.",
        )
