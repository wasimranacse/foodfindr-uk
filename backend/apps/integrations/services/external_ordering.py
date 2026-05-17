from urllib.parse import urlparse

from .base import IntegrationResult


ALLOWED_ORDERING_PROVIDERS = {
    "uber_eats": ("ubereats.com", "www.ubereats.com"),
    "deliveroo": ("deliveroo.co.uk", "www.deliveroo.co.uk", "deliveroo.com", "www.deliveroo.com"),
    "just_eat": ("just-eat.co.uk", "www.just-eat.co.uk", "just-eat.com", "www.just-eat.com"),
    "direct": (),
}


def validate_external_order_url(provider: str, url: str) -> bool:
    if not url:
        return True
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        return False
    allowed_hosts = ALLOWED_ORDERING_PROVIDERS.get(provider, ())
    if provider == "direct":
        return True
    return parsed.netloc.lower() in allowed_hosts


def get_ordering_url(restaurant, provider: str) -> IntegrationResult:
    url_by_provider = {
        "uber_eats": restaurant.uber_eats_url,
        "deliveroo": restaurant.deliveroo_url,
        "just_eat": restaurant.just_eat_url,
        "direct": restaurant.direct_order_url,
    }
    url = url_by_provider.get(provider, "")
    return IntegrationResult(
        configured=bool(url),
        provider=provider,
        data={"url": url},
        message="Restaurant-provided ordering URL." if url else "Ordering URL not provided.",
    )
