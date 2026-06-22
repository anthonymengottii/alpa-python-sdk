"""
Recurso de Saques
"""

from typing import Optional, Dict, Any
from ..http import HttpClient


class WithdrawalsResource:
    """Recurso para gerenciar Saques"""

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
        Lista saques

        Returns:
            Dicionário com 'data' (lista) e 'pagination'
        """
        params = {"page": page, "limit": limit, "cursor": cursor, "status": status}
        response = self.http.get("/withdraws", params)
        return {
            "data": response.get("withdraws") or response.get("data") or [],
            "pagination": response.get("pagination") or {"total": 0, "page": 1, "limit": 10},
        }

    def get(self, withdrawal_id: str) -> Dict[str, Any]:
        """Obtém um saque por ID"""
        if not withdrawal_id:
            raise ValueError("ID é obrigatório")
        return self.http.get(f"/withdraws/{withdrawal_id}")

    def get_balance(self) -> Dict[str, Any]:
        """
        Retorna o saldo disponível para saque

        Returns:
            Dicionário com availableCents, pendingCents, totalCents
        """
        return self.http.get("/withdraws/balance")

    def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Cria uma solicitação de saque

        Args:
            data:
                - amountCents: Valor em centavos (obrigatório, min 100)
                - pixKey: Chave PIX para recebimento
                - bankAccount: Dados bancários (bank, agency, account, accountType, document, name)
        """
        if not data.get("amountCents") or data.get("amountCents", 0) < 100:
            raise ValueError("Valor mínimo é R$ 1,00 (100 centavos)")
        if not data.get("pixKey") and not data.get("bankAccount"):
            raise ValueError("pixKey ou bankAccount é obrigatório")
        return self.http.post("/withdraws", data)

    def cancel(self, withdrawal_id: str) -> Dict[str, Any]:
        """Cancela um saque pendente"""
        if not withdrawal_id:
            raise ValueError("ID é obrigatório")
        return self.http.post(f"/withdraws/{withdrawal_id}/cancel")
