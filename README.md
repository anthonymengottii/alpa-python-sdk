<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="logo/light.png">
    <source media="(prefers-color-scheme: light)" srcset="logo/dark.png">
    <img src="logo/dark.png" alt="Alpa" height="60">
  </picture>
</p>

# Alpa Python SDK

SDK oficial da Alpa para Python. Integre PIX, cartão de crédito e boleto. Compatível com Python 3.8+ e frameworks como Flask e Django.

## 📦 Instalação

O SDK ainda não está publicado no PyPI. Instale direto do GitHub:

```bash
pip install git+https://github.com/anthonymengottii/alpa-python-sdk.git
```

## 🚀 Início rápido

```python
import os
from alpa import AlpaClient

alpa = AlpaClient(api_key=os.getenv("ALPA_API_KEY"))
```

> O ambiente (desenvolvimento ou produção) é determinado pela **chave** usada. O mesmo `base_url` (`https://alpa-sistema-api.onrender.com`) atende ambos.

### Criar um Link de Pagamento

```python
link = alpa.payment_links.create({
    "title": "Produto Premium",
    "amountCents": 9900,  # R$ 99,00
    "description": "Acesso vitalício",
})

print("Checkout:", alpa.payment_links.get_checkout_url(link["slug"]))  # https://checkout.usealpa.com/pay/abc123
```

### Criar uma Transação PIX

```python
tx = alpa.transactions.create({
    "product": "Curso Python",
    "amountCents": 19900,
    "paymentMethod": "PIX",
    "clientName": "João Silva",
    "clientEmail": "joao@example.com",
    "clientDocument": "12345678900",
})

print("PIX copia e cola:", tx["pixCopiaECola"])
```

### Validar Cupom

```python
result = alpa.coupons.validate(code="DESCONTO10", amount_cents=19900)

if result["valid"]:
    print("Desconto:", result["discountCents"] / 100)
    print("Final:", result["finalAmountCents"] / 100)
```

## 🔔 Webhooks

A Alpa assina cada webhook com **HMAC-SHA256 (hex)** no header `X-Webhook-Signature`. O envelope tem o formato `{ "id", "type", "data", "timestamp", "subscription" }`.

```python
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    signature = request.headers.get("x-webhook-signature")
    secret = os.getenv("ALPA_WEBHOOK_SECRET")

    if not alpa.verify_webhook_signature(request.data, signature, secret):
        return jsonify({"error": "Assinatura inválida"}), 401

    event = request.get_json()
    if event["type"] == "transaction.completed":
        # liberar produto / enviar email
        pass

    return jsonify({"received": True})
```

### Eventos disponíveis

`transaction.created`, `transaction.updated`, `transaction.completed`, `transaction.failed`, `transaction.refunded`, `payment_link.created`, `payment_link.updated`, `balance.updated`, `subscription.cancelled`, `kyc.submitted`, `kyc.approved`, `kyc.rejected`, `advance.created`, `advance.approved`, `advance.rejected`, `withdrawal.requested`, `withdrawal.completed`, `withdrawal.failed`.

Disponíveis via enum `WebhookEventType`.

## 🔧 Configuração

```python
alpa = AlpaClient(
    api_key="sua_api_key",                                 # Obrigatório
    base_url="https://alpa-sistema-api.onrender.com",      # Opcional
    version="v1",                                          # Opcional
    timeout=30,                                            # Opcional (segundos)
)
```

## 🛠️ Tratamento de Erros

```python
from alpa import (
    AlpaError,
    AlpaAuthenticationError,
    AlpaValidationError,
    AlpaNotFoundError,
    AlpaRateLimitError,
)

try:
    alpa.payment_links.create({"title": "Test", "amountCents": 9900})
except AlpaAuthenticationError as e:
    print("Erro de autenticação:", e.message)
except AlpaValidationError as e:
    print("Erro de validação:", e.message, e.details)
except AlpaError as e:
    print(f"Erro {e.status_code}:", e.message)
```

## 📚 Recursos disponíveis

`payment_links`, `transactions`, `products`, `coupons`, `clients`, `subscriptions`, `checkouts`, `offers`, `withdrawals`, `wallet`.

## 🧪 Testes

```bash
python -m pytest tests/
```

## 🔗 Links úteis

- [Documentação](https://docs.usealpa.com)
- [Dashboard](https://app.usealpa.com)
- [Suporte](mailto:suporte@usealpa.com)
- [Repositório](https://github.com/anthonymengottii/alpa-python-sdk)

## 📝 Licença

MIT
