"""
Recurso de Ofertas (Order Bumps, Upsell, Downsell)
"""

from typing import Optional, Dict, Any, List
from ..http import HttpClient


class OffersResource:
    """Recurso para gerenciar Order Bumps, Upsell e Downsell"""

    def __init__(self, http: HttpClient):
        self.http = http

    # ── Order Bumps ──────────────────────────────────────────────────────────

    def list_order_bumps(self, checkout_id: str) -> List[Dict[str, Any]]:
        """Lista order bumps de um checkout"""
        if not checkout_id:
            raise ValueError("checkout_id é obrigatório")
        response = self.http.get(f"/checkouts/{checkout_id}/order-bumps")
        if isinstance(response, list):
            return response
        return response.get("orderBumps") or response.get("data") or []

    def create_order_bump(self, checkout_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Cria um order bump em um checkout

        Args:
            checkout_id: ID do checkout
            data:
                - productId: ID do produto (obrigatório)
                - title: Título personalizado
                - description: Descrição
                - discountCents: Desconto em centavos
                - discountPercentage: Desconto percentual
                - position: Posição de exibição
        """
        if not checkout_id:
            raise ValueError("checkout_id é obrigatório")
        if not data.get("productId"):
            raise ValueError("productId é obrigatório")
        return self.http.post(f"/checkouts/{checkout_id}/order-bumps", data)

    def update_order_bump(
        self, checkout_id: str, bump_id: str, data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Atualiza um order bump"""
        if not checkout_id:
            raise ValueError("checkout_id é obrigatório")
        if not bump_id:
            raise ValueError("bump_id é obrigatório")
        return self.http.request(
            "PUT", f"/checkouts/{checkout_id}/order-bumps/{bump_id}", data=data
        )

    def delete_order_bump(self, checkout_id: str, bump_id: str) -> None:
        """Remove um order bump"""
        if not checkout_id:
            raise ValueError("checkout_id é obrigatório")
        if not bump_id:
            raise ValueError("bump_id é obrigatório")
        self.http.delete(f"/checkouts/{checkout_id}/order-bumps/{bump_id}")

    # ── Upsell ───────────────────────────────────────────────────────────────

    def get_upsell(self, checkout_id: str) -> Optional[Dict[str, Any]]:
        """Obtém o upsell de um checkout"""
        if not checkout_id:
            raise ValueError("checkout_id é obrigatório")
        response = self.http.get(f"/checkouts/{checkout_id}/upsell")
        return response or None

    def upsert_upsell(self, checkout_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Cria ou atualiza o upsell de um checkout

        Args:
            checkout_id: ID do checkout
            data:
                - productId: ID do produto (obrigatório)
                - title, description, discountCents, discountPercentage
        """
        if not checkout_id:
            raise ValueError("checkout_id é obrigatório")
        if not data.get("productId"):
            raise ValueError("productId é obrigatório")
        return self.http.post(f"/checkouts/{checkout_id}/upsell", data)

    def delete_upsell(self, checkout_id: str) -> None:
        """Remove o upsell de um checkout"""
        if not checkout_id:
            raise ValueError("checkout_id é obrigatório")
        self.http.delete(f"/checkouts/{checkout_id}/upsell")

    # ── Downsell ─────────────────────────────────────────────────────────────

    def upsert_downsell(self, checkout_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Cria ou atualiza o downsell de um checkout

        Args:
            checkout_id: ID do checkout
            data:
                - productId: ID do produto (obrigatório)
                - title, description, discountCents, discountPercentage
        """
        if not checkout_id:
            raise ValueError("checkout_id é obrigatório")
        if not data.get("productId"):
            raise ValueError("productId é obrigatório")
        return self.http.post(f"/checkouts/{checkout_id}/upsell/downsell", data)

    def delete_downsell(self, checkout_id: str) -> None:
        """Remove o downsell de um checkout"""
        if not checkout_id:
            raise ValueError("checkout_id é obrigatório")
        self.http.delete(f"/checkouts/{checkout_id}/upsell/downsell")
