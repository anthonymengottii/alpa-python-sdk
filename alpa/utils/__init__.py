"""
Utilitários do SDK Alpa
"""

from .errors import (
    AlpaError,
    AlpaAuthenticationError,
    AlpaValidationError,
    AlpaNotFoundError,
    AlpaRateLimitError,
    AlpaServerError,
    handle_api_error
)
from .webhooks import verify_webhook_signature, extract_webhook_signature, WebhookEventType

__all__ = [
    'AlpaError',
    'AlpaAuthenticationError',
    'AlpaValidationError',
    'AlpaNotFoundError',
    'AlpaRateLimitError',
    'AlpaServerError',
    'handle_api_error',
    'verify_webhook_signature',
    'extract_webhook_signature',
    'WebhookEventType',
]
