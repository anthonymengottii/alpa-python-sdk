"""
Recurso de Assinaturas
"""

from typing import Optional, Dict, Any
from ..http import HttpClient


class SubscriptionsResource:
    """Recurso para gerenciar Assinaturas recorrentes"""

    def __init__(self, http: HttpClient):
        self.http = http

    def list(
        self,
        page: Optional[int] = None,
        limit: Optional[int] = None,
        cursor: Optional[str] = None,
        status: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Lista assinaturas

        Returns:
            Dicionário com 'data' (lista) e 'pagination'
        """
        params = {"page": page, "limit": limit, "cursor": cursor, "status": status}
        response = self.http.get("/subscriptions", params)
        return {
            "data": response.get("subscriptions") or response.get("data") or [],
            "pagination": response.get("pagination") or {"total": 0, "page": 1, "limit": 10},
        }

    def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Cria uma assinatura

        Args:
            data:
                - planId: ID do plano (obrigatório)
                - clientId: ID do cliente existente
                - client: Dados do novo cliente (name, email, document, phone)
                - paymentMethod: CREDIT_CARD | PIX | BOLETO
                - couponCode: Código do cupom
                - metadata: Metadados adicionais
        """
        if not data.get("planId"):
            raise ValueError("planId é obrigatório")
        if data.get("client") and not data["client"].get("email"):
            raise ValueError("Email do cliente é obrigatório")
        return self.http.post("/subscriptions", data)

    def cancel(self, subscription_id: str) -> Dict[str, Any]:
        """Cancela uma assinatura"""
        if not subscription_id:
            raise ValueError("ID é obrigatório")
        return self.http.patch(f"/subscriptions/{subscription_id}/cancel")

    def pause(self, subscription_id: str) -> Dict[str, Any]:
        """Pausa uma assinatura"""
        if not subscription_id:
            raise ValueError("ID é obrigatório")
        return self.http.patch(f"/subscriptions/{subscription_id}/pause")

    def resume(self, subscription_id: str) -> Dict[str, Any]:
        """Retoma uma assinatura pausada"""
        if not subscription_id:
            raise ValueError("ID é obrigatório")
        return self.http.patch(f"/subscriptions/{subscription_id}/resume")

    def retry(self, subscription_id: str) -> Dict[str, Any]:
        """Tenta reprocessar o pagamento de uma assinatura em atraso"""
        if not subscription_id:
            raise ValueError("ID é obrigatório")
        return self.http.post(f"/subscriptions/{subscription_id}/retry")

    def get_metrics(self) -> Dict[str, Any]:
        """Retorna métricas de assinaturas (MRR, churn, totais)"""
        return self.http.get("/subscriptions/metrics")
