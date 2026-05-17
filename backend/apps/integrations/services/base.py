from dataclasses import dataclass, field


@dataclass(frozen=True)
class IntegrationResult:
    configured: bool
    provider: str
    data: dict = field(default_factory=dict)
    message: str = ""


def not_configured(provider: str) -> IntegrationResult:
    return IntegrationResult(
        configured=False,
        provider=provider,
        message=f"{provider} integration is not configured.",
    )
