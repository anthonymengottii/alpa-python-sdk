"""
Exemplo básico de uso do SDK Alpa Python
"""

import os
from alpa import AlpaClient

# Inicializar o cliente
alpa = AlpaClient(
    api_key=os.getenv("ALPA_API_KEY", "sua_api_key_aqui"),
)


def exemplo_payment_links():
    """Exemplo de uso de Payment Links"""
    print("=== Exemplo: Payment Links ===\n")

    # Criar um link de pagamento
    print("1. Criando link de pagamento...")
    payment_link = alpa.payment_links.create({
        "title": "Produto Premium",
        "amountCents": 9900,  # R$ 99,00
        "description": "Descrição do produto",
        "status": "ACTIVE"
    })
    print(f"   Link criado: {payment_link.get('id')}")
    print(f"   URL: {payment_link.get('url')}\n")

    # Listar links
    print("2. Listando links de pagamento...")
    links = alpa.payment_links.list(page=1, limit=5)
    print(f"   Total de links: {links['pagination'].get('total', 0)}")
    if links['data']:
        print(f"   Primeiro link: {links['data'][0].get('title')}\n")

    # Deletar o link de teste
    print("3. Deletando link de teste...")
    try:
        alpa.payment_links.delete(payment_link['id'])
        print("   Link deletado com sucesso\n")
    except Exception as e:
        print(f"   Erro ao deletar: {e}\n")


def exemplo_transacao_pix():
    """Exemplo de criação de transação PIX"""
    print("=== Exemplo: Transação PIX ===\n")

    tx = alpa.transactions.create({
        "product": "Curso Online",
        "amountCents": 19900,  # R$ 199,00
        "paymentMethod": "PIX",
        "clientName": "João Silva",
        "clientEmail": "joao@example.com",
        "clientDocument": "12345678900",
    })
    print(f"   Transação: {tx.get('id')} ({tx.get('status')})")
    print(f"   PIX copia e cola: {tx.get('pixCopiaECola')}\n")


def exemplo_cupons():
    """Exemplo de uso de Cupons"""
    print("=== Exemplo: Cupons ===\n")

    print("1. Validando cupom...")
    try:
        validation = alpa.coupons.validate(
            code="CUPOMTESTE",
            amount_cents=10000
        )
        if validation['valid']:
            print("   Cupom válido!")
            print(f"   Desconto: R$ {validation['discountCents'] / 100:.2f}")
            print(f"   Valor final: R$ {validation['finalAmountCents'] / 100:.2f}\n")
        else:
            print(f"   Cupom inválido: {validation.get('message')}\n")
    except Exception as e:
        print(f"   Erro: {e}\n")


if __name__ == "__main__":
    print("🧪 Testando SDK Alpa Python\n")

    try:
        exemplo_payment_links()
        exemplo_transacao_pix()
        exemplo_cupons()

        print("✅ Todos os exemplos executados com sucesso!")
    except Exception as e:
        print(f"\n❌ Erro durante os testes: {e}")
        import traceback
        traceback.print_exc()
