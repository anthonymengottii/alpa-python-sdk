"""
Utilitários para verificação de webhooks
"""

import hmac
import hashlib
from typing import Dict, Optional, Union
from enum import Enum


class WebhookEventType(str, Enum):
    """
    Tipos de eventos de webhook assináveis na Alpa.

    Conjunto alinhado ao backend. O envelope entregue tem o formato
    ``{ "id", "type", "data", "timestamp", "subscription" }``.
    """
    TRANSACTION_CREATED = "transaction.created"
    TRANSACTION_UPDATED = "transaction.updated"
    TRANSACTION_COMPLETED = "transaction.completed"
    TRANSACTION_FAILED = "transaction.failed"
    TRANSACTION_REFUNDED = "transaction.refunded"
    PAYMENT_LINK_CREATED = "payment_link.created"
    PAYMENT_LINK_UPDATED = "payment_link.updated"
    BALANCE_UPDATED = "balance.updated"
    SUBSCRIPTION_CANCELLED = "subscription.cancelled"
    KYC_SUBMITTED = "kyc.submitted"
    KYC_APPROVED = "kyc.approved"
    KYC_REJECTED = "kyc.rejected"
    ADVANCE_CREATED = "advance.created"
    ADVANCE_APPROVED = "advance.approved"
    ADVANCE_REJECTED = "advance.rejected"
    WITHDRAWAL_REQUESTED = "withdrawal.requested"
    WITHDRAWAL_COMPLETED = "withdrawal.completed"
    WITHDRAWAL_FAILED = "withdrawal.failed"


def verify_webhook_signature(
    payload: Union[bytes, str],
    signature: str,
    secret: str
) -> bool:
    """
    Verifica a assinatura de um webhook usando HMAC SHA256 (hex).

    A Alpa envia a assinatura em hexadecimal no header
    ``X-Webhook-Signature`` (prefixada por ``sha256=``).

    Args:
        payload: Corpo bruto da requisição (bytes ou string)
        signature: Assinatura recebida no header (com ou sem prefixo ``sha256=``)
        secret: Secret da assinatura de webhook

    Returns:
        True se a assinatura for válida
    """
    if payload is None or not signature or not secret:
        return False

    try:
        normalized_signature = signature.replace("sha256=", "")
        if not normalized_signature:
            return False

        # Converte payload para bytes se necessário
        if isinstance(payload, str):
            payload_bytes = payload.encode('utf-8')
        else:
            payload_bytes = payload

        # Gera o hash HMAC SHA256
        hash_obj = hmac.new(
            secret.encode('utf-8'),
            payload_bytes,
            hashlib.sha256
        )
        expected_signature = hash_obj.hexdigest()

        # Comparação segura para prevenir timing attacks
        return hmac.compare_digest(expected_signature, normalized_signature)
    except Exception:
        return False


def extract_webhook_signature(headers: Dict[str, Union[str, list, None]]) -> Optional[str]:
    """
    Extrai a assinatura do header da requisição.

    O header canônico da Alpa é ``x-webhook-signature``. Nomes legados são
    aceitos como fallback.

    Args:
        headers: Headers da requisição

    Returns:
        A assinatura (sem prefixo ``sha256=``) ou None se não encontrada
    """
    signature_header = (
        headers.get("x-webhook-signature") or
        headers.get("X-Webhook-Signature") or
        headers.get("x-alpa-signature") or
        headers.get("x-upay-signature") or
        headers.get("signature")
    )

    if not signature_header:
        return None

    # Se for lista, pega o primeiro
    if isinstance(signature_header, list):
        signature_header = signature_header[0] if signature_header else None

    if not signature_header:
        return None

    # Remove prefixo "sha256=" se existir
    return signature_header.replace("sha256=", "")
