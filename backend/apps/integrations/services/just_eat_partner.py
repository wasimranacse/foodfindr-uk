from django.conf import settings

from .base import IntegrationResult, not_configured


class JustEatPartnerClient:
    provider = "Just Eat partner API"

    def __init__(self, api_key: str | None = None):
        self.api_key = api_key if api_key is not None else getattr(settings, "JUST_EAT_API_KEY", "")

    @property
    def is_configured(self) -> bool:
        return bool(self.api_key)

    def get_restaurant_status(self, **payload) -> IntegrationResult:
        if not self.is_configured:
            return not_configured(self.provider)
        return IntegrationResult(
            configured=True,
            provider=self.provider,
            data=payload,
            message="Just Eat partner API placeholder ready for backend-only implementation.",
        )
