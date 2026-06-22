"""
Testes unitários do SDK Alpa (sem chamadas de rede — HttpClient mockado).
"""

from unittest.mock import MagicMock

import pytest

from alpa import (
    AlpaClient,
    AlpaError,
    WebhookEventType,
    verify_webhook_signature,
    extract_webhook_signature,
)
from alpa.resources.payment_links import PaymentLinksResource
from alpa.resources.transactions import TransactionsResource
from alpa.resources.products import ProductsResource
import hmac
import hashlib


def make_http():
    http = MagicMock()
    http.base_url = "https://test.example.com"
    return http


# ─── Client ──────────────────────────────────────────────────────────────

def test_client_requires_api_key():
    with pytest.raises(ValueError):
        AlpaClient(api_key="")


def test_client_exposes_resources():
    client = AlpaClient(api_key="key")
    assert client.payment_links is not None
    assert client.transactions is not None


# ─── Payment Links ───────────────────────────────────────────────────────

def test_payment_link_create_sends_amount_cents():
    http = make_http()
    http.post.return_value = {"id": "lnk_1", "url": "https://checkout.usealpa.com/pay/abc"}
    res = PaymentLinksResource(http)

    result = res.create({"title": "Produto Premium", "amountCents": 9900})

    args, _ = http.post.call_args
    assert args[0] == "/payment-links"
    assert args[1]["amountCents"] == 9900
    assert result["url"] == "https://checkout.usealpa.com/pay/abc"


def test_payment_link_create_accepts_amount_alias():
    http = make_http()
    http.post.return_value = {"id": "lnk_2"}
    res = PaymentLinksResource(http)

    res.create({"title": "Legado", "amount": 5000})

    args, _ = http.post.call_args
    assert args[1]["amountCents"] == 5000


def test_payment_link_create_title_too_short():
    res = PaymentLinksResource(make_http())
    with pytest.raises(ValueError):
        res.create({"title": "ab", "amountCents": 9900})


def test_payment_link_checkout_url_domain():
    res = PaymentLinksResource(make_http())
    assert res.get_checkout_url("meu-slug") == "https://checkout.usealpa.com/pay/meu-slug"


# ─── Transactions ────────────────────────────────────────────────────────

def test_transaction_create_flat_client():
    http = make_http()
    http.post.return_value = {"id": "tx_1", "pixCopiaECola": "000201..."}
    res = TransactionsResource(http)

    result = res.create({
        "product": "Curso",
        "amountCents": 19900,
        "paymentMethod": "PIX",
        "clientEmail": "joao@example.com",
    })

    args, _ = http.post.call_args
    assert args[0] == "/transactions"
    assert args[1]["clientEmail"] == "joao@example.com"
    assert result["pixCopiaECola"] == "000201..."


def test_transaction_create_requires_client_email():
    res = TransactionsResource(make_http())
    with pytest.raises(ValueError):
        res.create({"product": "X", "amountCents": 19900})


# ─── Products ────────────────────────────────────────────────────────────

def test_product_create_min_price():
    res = ProductsResource(make_http())
    with pytest.raises(ValueError):
        res.create({"name": "X", "price": 50})


# ─── Webhooks ────────────────────────────────────────────────────────────

def test_verify_webhook_signature_valid_with_prefix():
    secret = "test-secret"
    payload = '{"type":"transaction.completed"}'
    sig = hmac.new(secret.encode(), payload.encode(), hashlib.sha256).hexdigest()
    assert verify_webhook_signature(payload, f"sha256={sig}", secret) is True


def test_verify_webhook_signature_invalid():
    assert verify_webhook_signature("{}", "bad", "secret") is False


def test_extract_webhook_signature_canonical_header():
    assert extract_webhook_signature({"x-webhook-signature": "sha256=abc"}) == "abc"


def test_extract_webhook_signature_legacy_fallback():
    assert extract_webhook_signature({"x-upay-signature": "legacy"}) == "legacy"


def test_event_enum_aligned():
    assert WebhookEventType.TRANSACTION_COMPLETED.value == "transaction.completed"
    assert "transaction.paid" not in [e.value for e in WebhookEventType]


def test_errors_have_status_code_alias():
    err = AlpaError("x", status=400)
    assert err.status_code == 400
