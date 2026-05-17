from django.conf import settings

from .base import IntegrationResult, not_configured


class FoodHygieneRatingClient:
    provider = "Food Standards Agency Food Hygiene Rating API"

    def __init__(self, base_url: str | None = None):
        self.base_url = base_url if base_url is not None else getattr(settings, "FSA_API_BASE_URL", "")

    @property
    def is_configured(self) -> bool:
        return bool(self.base_url)

    def lookup_business(self, *, fsa_business_id: str = "", postcode: str = "", name: str = "") -> IntegrationResult:
        if not self.is_configured:
            return not_configured(self.provider)
        return IntegrationResult(
            configured=True,
            provider=self.provider,
            data={
                "fsa_business_id": fsa_business_id,
                "postcode": postcode,
                "name": name,
            },
            message="FSA lookup placeholder ready for backend-only implementation.",
        )
