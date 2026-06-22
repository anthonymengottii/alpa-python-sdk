"""
Recurso de Carteira
"""

from typing import Optional, Dict, Any
from ..http import HttpClient


class WalletResource:
    """Recurso para consultar a Carteira"""

    def __init__(self, http: HttpClient):
        self.http = http

    def get_summary(self) -> Dict[str, Any]:
        """
        Retorna o resumo da carteira

        Returns:
            Dicionário com balanceCents, pendingCents, totalReceivedCents, totalWithdrawnCents
        """
        return self.http.get("/wallet/summary")

    def get_statement(
        self,
        page: Optional[int] = None,
        limit: Optional[int] = None,
        cursor: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Retorna o extrato da carteira

        Args:
            page: Número da página
            limit: Limite de itens por página
            cursor: Cursor para paginação
            start_date: Data inicial (ISO 8601)
            end_date: Data final (ISO 8601)

        Returns:
            Dicionário com 'data' (lista de entradas) e 'pagination'
        """
        params = {
            "page": page,
            "limit": limit,
            "cursor": cursor,
            "startDate": start_date,
            "endDate": end_date,
        }
        response = self.http.get("/wallet/statement", params)
        return {
            "data": response.get("entries") or response.get("data") or [],
            "pagination": response.get("pagination") or {"total": 0, "page": 1, "limit": 10},
        }
