"""
Script de teste manual do SDK Alpa Python (faz chamadas reais à API).

Para testes unitários (sem rede), use: python -m pytest tests/
"""

import os
import sys

# Adiciona o diretório atual ao path para importar o módulo
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from alpa import AlpaClient

# Configure via variável de ambiente
API_KEY = os.getenv("ALPA_API_KEY", "sua_api_key_aqui")
BASE_URL = os.getenv("ALPA_BASE_URL", "https://alpa-sistema-api.onrender.com")


def test_sdk():
    """Testa o SDK Alpa Python"""
    print("Testando SDK Alpa Python...\n")
    print(f"Usando base URL: {BASE_URL}\n")

    alpa = AlpaClient(api_key=API_KEY, base_url=BASE_URL, version="v1")

    try:
        # Teste 1: Listar Payment Links
        print("Teste 1: Listar Payment Links...")
        try:
            links = alpa.payment_links.list(page=1, limit=5)
            print(f"[OK] Encontrados {links['pagination'].get('total', len(links['data']))} links")
            if links['data']:
                first_link = links['data'][0]
                print(f"   Primeiro link: {first_link.get('title')}")
                print(f"   URL: {first_link.get('url')}")
        except Exception as e:
            print(f"[ERRO] {e}")

        # Teste 2: Listar Transações
        print("\nTeste 2: Listar Transacoes...")
        try:
            transactions = alpa.transactions.list(page=1, limit=5)
            total = transactions['pagination'].get('total', len(transactions['data']))
            print(f"[OK] Encontradas {total} transacoes")
            if transactions['data']:
                tx = transactions['data'][0]
                amount = tx.get('amountCents', 0) / 100
                print(f"   Primeira: {tx.get('product')} - R$ {amount:.2f} - {tx.get('status')}")
        except Exception as e:
            print(f"[ERRO] {e}")

        # Teste 3: Criar e Deletar Payment Link
        print("\nTeste 3: Criar e Deletar Payment Link...")
        try:
            from datetime import datetime
            test_link = alpa.payment_links.create({
                "title": f"Teste SDK Python - {datetime.now().isoformat()}",
                "description": "Link criado pelo teste do SDK Python",
                "amountCents": 2500,  # R$ 25,00
                "status": "INACTIVE"
            })
            print(f"[OK] Link criado! ID: {test_link.get('id')} URL: {test_link.get('url')}")
            try:
                alpa.payment_links.delete(test_link['id'])
                print("   [OK] Link de teste deletado")
            except Exception as delete_error:
                print(f"   [AVISO] Nao foi possivel deletar: {delete_error}")
        except Exception as e:
            print(f"[ERRO] {e}")

        print("\n[OK] Testes concluidos!")

    except Exception as e:
        print(f"\n[ERRO] Erro geral: {e}")


if __name__ == "__main__":
    test_sdk()
