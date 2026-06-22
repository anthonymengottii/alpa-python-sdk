"""
Recurso de Transações
"""

from typing import Optional, Dict, Any
from ..http import HttpClient


class TransactionsResource:
    """Recurso para gerenciar Transações"""
    
    def __init__(self, http: HttpClient):
        self.http = http
    
    def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Cria uma nova transação
        
        Args:
            data: Dados da transação
                - product: Nome do produto (obrigatório)
                - amountCents: Valor em centavos (obrigatório, min 100)
                - paymentMethod: Método de pagamento (PIX, CARD, BOLETO)
                - clientName / clientEmail / clientDocument / clientPhone: dados do cliente
                - paymentLinkId: ID do link de pagamento
                - installments: parcelas (cartão)
                - metadata: Metadados adicionais
                - couponCode: Código do cupom

        Returns:
            Transação criada (PIX retorna ``pixCopiaECola`` e ``pixExpiresAt``)
        """
        # Validação básica
        if not data.get("product") or len(str(data["product"]).strip()) == 0:
            raise ValueError("Produto é obrigatório")

        if not data.get("amountCents") or data.get("amountCents", 0) < 100:
            raise ValueError("Valor mínimo é R$ 1,00 (100 centavos)")

        if not data.get("clientEmail"):
            raise ValueError("clientEmail é obrigatório")

        return self.http.post("/transactions", data)
    
    def list(
        self,
        page: Optional[int] = None,
        limit: Optional[int] = None,
        cursor: Optional[str] = None,
        order_by: Optional[str] = None,
        order_direction: Optional[str] = None,
        status: Optional[str] = None,
        payment_method: Optional[str] = None,
        client_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Lista transações
        
        Args:
            page: Número da página
            limit: Limite de itens por página
            cursor: Cursor para paginação
            order_by: Campo para ordenação
            order_direction: Direção da ordenação (ASC ou DESC)
            status: Filtrar por status
            payment_method: Filtrar por método de pagamento
            client_id: Filtrar por cliente
            
        Returns:
            Dicionário com 'data' (lista) e 'pagination'
        """
        params = {
            "page": page,
            "limit": limit,
            "cursor": cursor,
            "orderBy": order_by,
            "orderDirection": order_direction,
            "status": status,
            "method": payment_method,
            "clientId": client_id,
        }
        
        response = self.http.get("/transactions", params)
        return {
            "data": response.get("transactions") or response.get("data") or [],
            "pagination": response.get("pagination") or {"total": 0, "page": 1, "limit": 10},
        }
    
    def get(self, transaction_id: str) -> Dict[str, Any]:
        """
        Obtém uma transação por ID
        
        Args:
            transaction_id: ID da transação
            
        Returns:
            Transação
        """
        if not transaction_id:
            raise ValueError("ID é obrigatório")
        
        return self.http.get(f"/transactions/{transaction_id}")
    
    def process(
        self,
        transaction_id: str,
        payment_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Processa o pagamento de uma transação
        
        Args:
            transaction_id: ID da transação
            payment_data: Dados do pagamento (cardData, installments)
            
        Returns:
            Transação processada
        """
        if not transaction_id:
            raise ValueError("ID é obrigatório")
        
        return self.http.post(f"/transactions/{transaction_id}/process", payment_data)
    
    def capture(self, transaction_id: str) -> Dict[str, Any]:
        """
        Captura uma transação autorizada (Pagar.me)
        
        Args:
            transaction_id: ID da transação
            
        Returns:
            Transação capturada
        """
        if not transaction_id:
            raise ValueError("ID é obrigatório")
        
        return self.http.post(f"/transactions/{transaction_id}/capture")
    
    def cancel(self, transaction_id: str) -> Dict[str, Any]:
        """
        Cancela uma transação pendente
        
        Args:
            transaction_id: ID da transação
            
        Returns:
            Transação cancelada
        """
        if not transaction_id:
            raise ValueError("ID é obrigatório")
        
        return self.http.post(f"/transactions/{transaction_id}/cancel")
    
    def refund(
        self,
        transaction_id: str,
        amount_cents: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Estorna uma transação paga
        
        Args:
            transaction_id: ID da transação
            amount_cents: Valor a estornar em centavos (opcional, estorna tudo se não informado)
            
        Returns:
            Transação estornada
        """
        if not transaction_id:
            raise ValueError("ID é obrigatório")
        
        data = {}
        if amount_cents is not None:
            data["amountCents"] = amount_cents
        
        return self.http.post(f"/transactions/{transaction_id}/refund", data)
