"""
Recurso de Checkouts
"""

from typing import Optional, Dict, Any
from ..http import HttpClient


class CheckoutsResource:
    """Recurso para gerenciar Checkouts"""

    def __init__(self, http: HttpClient):
        self.http = http

    def list(
        self,
        page: Optional[int] = None,
        limit: Optional[int] = None,
        cursor: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Lista checkouts

        Returns:
            Dicionário com 'data' (lista) e 'pagination'
        """
        params = {"page": page, "limit": limit, "cursor": cursor}
        response = self.http.get("/checkouts", params)
        return {
            "data": response.get("checkouts") or response.get("data") or [],
            "pagination": response.get("pagination") or {"total": 0, "page": 1, "limit": 10},
        }

    def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Cria um checkout

        Args:
            data:
                - name: Nome do checkout (obrigatório)
                - paymentLinkId: ID do link de pagamento
                - settings: Configurações do checkout
                - customization: Personalização visual
        """
        if not data.get("name") or len(str(data["name"]).strip()) == 0:
            raise ValueError("Nome do checkout é obrigatório")
        return self.http.post("/checkouts", data)

    def get(self, checkout_id: str) -> Dict[str, Any]:
        """Obtém um checkout por ID"""
        if not checkout_id:
            raise ValueError("ID é obrigatório")
        return self.http.get(f"/checkouts/{checkout_id}")

    def update(self, checkout_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Atualiza um checkout"""
        if not checkout_id:
            raise ValueError("ID é obrigatório")
        return self.http.request("PUT", f"/checkouts/{checkout_id}", data=data)

    def delete(self, checkout_id: str) -> None:
        """Deleta um checkout"""
        if not checkout_id:
            raise ValueError("ID é obrigatório")
        self.http.delete(f"/checkouts/{checkout_id}")
