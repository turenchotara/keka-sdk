from dataclasses import dataclass, field
from typing import FrozenSet, Optional
from urllib.parse import urlparse, urlunparse

DEFAULT_RETRY_STATUS_CODES: FrozenSet[int] = frozenset({429, 500, 502, 503, 504})
TOKEN_PATH = "/connect/token"


def derive_login_url(instance_url: str, login_url: Optional[str] = None) -> str:
    """
    Derive the OAuth token endpoint from an instance URL.

    For an instance like ``https://mycompany.keka.com`` this returns
    ``https://login.keka.com/connect/token``. When ``login_url`` is provided it
    is used verbatim, allowing on-prem/custom deployments.
    """
    if login_url:
        return login_url

    parsed = urlparse(instance_url if "//" in instance_url else f"https://{instance_url}")
    host = parsed.hostname
    if not host:
        raise ValueError(f"Could not derive login URL from instance_url: {instance_url!r}")

    labels = host.split(".")
    base_domain = ".".join(labels[-2:]) if len(labels) >= 2 else host
    login_host = f"login.{base_domain}"
    port = f":{parsed.port}" if parsed.port else ""

    return urlunparse((parsed.scheme or "https", f"{login_host}{port}", TOKEN_PATH, "", "", ""))


@dataclass
class KekaConfig:
    """
    Central configuration for a Keka client.

    Args:
        instance_url: Base URL of the Keka tenant (e.g. ``https://acme.keka.com``).
        login_url: Explicit OAuth token endpoint. Derived from ``instance_url``
            when omitted.
        timeout: Per-request timeout in seconds.
        max_retries: Maximum number of retry attempts for transient failures.
        retry_delay: Initial backoff delay in seconds.
        backoff_factor: Multiplier applied to the delay on each retry.
        max_backoff: Upper bound (seconds) on any single backoff sleep.
        jitter: Maximum random jitter (seconds) added to each backoff sleep.
        retry_status_codes: HTTP status codes that trigger a retry.
    """

    instance_url: str
    login_url: Optional[str] = None
    timeout: float = 30.0
    max_retries: int = 3
    retry_delay: float = 1.0
    backoff_factor: float = 2.0
    max_backoff: float = 30.0
    jitter: float = 0.5
    retry_status_codes: FrozenSet[int] = field(default_factory=lambda: DEFAULT_RETRY_STATUS_CODES)

    def __post_init__(self) -> None:
        if not self.instance_url:
            raise ValueError("instance_url is required")
        self.instance_url = self.instance_url.rstrip("/")

    @property
    def token_url(self) -> str:
        """The fully-resolved OAuth token endpoint."""
        return derive_login_url(self.instance_url, self.login_url)
