"""
SDK oficial da Alpa para Python
"""

from .client import AlpaClient
from .utils import (
    AlpaError,
    AlpaAuthenticationError,
    AlpaValidationError,
    AlpaNotFoundError,
    AlpaRateLimitError,
    AlpaServerError,
    verify_webhook_signature,
    extract_webhook_signature,
    WebhookEventType,
)

__version__ = "2.0.0"

__all__ = [
    "AlpaClient",
    "AlpaError",
    "AlpaAuthenticationError",
    "AlpaValidationError",
    "AlpaNotFoundError",
    "AlpaRateLimitError",
    "AlpaServerError",
    "verify_webhook_signature",
    "extract_webhook_signature",
    "WebhookEventType",
]
