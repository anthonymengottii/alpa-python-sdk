"""
Recurso de Payment Links
"""

from typing import Optional, Dict, Any
from ..http import HttpClient


class PaymentLinksResource:
    """Recurso para gerenciar Payment Links"""
    
    def __init__(self, http: HttpClient):
        self.http = http
    
    def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Cria um novo link de pagamento
        
        Args:
            data: Dados do link de pagamento
                - title: Título do link (obrigatório, min 3 caracteres)
                - amount: Valor em centavos (obrigatório se não houver products)
                - description: Descrição do link
                - currency: Moeda (padrão: BRL)
                - expiresAt: Data de expiração (ISO string)
                - redirectUrl: URL de redirecionamento
                - settings: Configurações de pagamento
                - status: Status (ACTIVE ou INACTIVE)
                - products: Lista de produtos
                
        Returns:
            Link de pagamento criado
        """
        # Validação básica
        if not data.get("title") or len(data["title"].strip()) < 3:
            raise ValueError("Título deve ter pelo menos 3 caracteres")

        # amountCents é o canônico; "amount" é alias deprecado.
        amount_cents = data.get("amountCents", data.get("amount"))

        if not amount_cents and not data.get("products"):
            raise ValueError("É necessário fornecer amountCents ou products")

        if amount_cents and amount_cents < 100:
            raise ValueError("Valor mínimo é R$ 1,00 (100 centavos)")

        # Prepara dados para envio
        request_data = {
            "title": data["title"],
            "description": data.get("description"),
            "amountCents": amount_cents,
            "products": data.get("products"),
            "currency": data.get("currency", "BRL"),
            "expiresAt": data.get("expiresAt"),
            "redirectUrl": data.get("redirectUrl"),
            "settings": data.get("settings"),
            "status": data.get("status", "ACTIVE"),
            "metaPixelCode": data.get("metaPixelCode"),
            "stockQuantity": data.get("stockQuantity"),
            "stockEnabled": data.get("stockEnabled"),
        }

        # Remove valores None
        request_data = {k: v for k, v in request_data.items() if v is not None}

        response = self.http.post("/payment-links", request_data)
        return response.get("paymentLink") or response.get("data") or response
    
    def list(
        self,
        page: Optional[int] = None,
        limit: Optional[int] = None,
        cursor: Optional[str] = None,
        order_by: Optional[str] = None,
        order_direction: Optional[str] = None,
        status: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Lista links de pagamento
        
        Args:
            page: Número da página
            limit: Limite de itens por página
            cursor: Cursor para paginação
            order_by: Campo para ordenação
            order_direction: Direção da ordenação (ASC ou DESC)
            status: Filtrar por status
            
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
        }
        
        response = self.http.get("/payment-links", params)
        return {
            "data": response.get("paymentLinks") or response.get("data") or [],
            "pagination": response.get("pagination") or {"total": 0, "page": 1, "limit": 10},
        }
    
    def get(self, link_id: str) -> Dict[str, Any]:
        """
        Obtém um link de pagamento por ID
        
        Args:
            link_id: ID do link de pagamento
            
        Returns:
            Link de pagamento
        """
        if not link_id:
            raise ValueError("ID é obrigatório")
        
        response = self.http.get(f"/payment-links/{link_id}")
        return response.get("paymentLink") or response.get("data") or response
    
    def get_by_slug(self, slug: str) -> Dict[str, Any]:
        """
        Obtém um link de pagamento por slug
        
        Args:
            slug: Slug do link de pagamento
            
        Returns:
            Link de pagamento
        """
        if not slug:
            raise ValueError("Slug é obrigatório")
        
        return self.http.get(f"/payment-links/slug/{slug}")
    
    def update(self, link_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Atualiza um link de pagamento
        
        Args:
            link_id: ID do link de pagamento
            data: Dados para atualizar
            
        Returns:
            Link de pagamento atualizado
        """
        if not link_id:
            raise ValueError("ID é obrigatório")
        
        # Prepara dados para envio
        update_data = {}
        if "title" in data:
            update_data["title"] = data["title"]
        if "description" in data:
            update_data["description"] = data["description"]
        if "amountCents" in data or "amount" in data:
            update_data["amountCents"] = data.get("amountCents", data.get("amount"))
        if "status" in data:
            update_data["status"] = data["status"]
        if "expiresAt" in data:
            update_data["expiresAt"] = data["expiresAt"]
        if "redirectUrl" in data:
            update_data["redirectUrl"] = data["redirectUrl"]
        if "settings" in data:
            update_data["settings"] = data["settings"]
        
        return self.http.patch(f"/payment-links/{link_id}", update_data)
    
    def delete(self, link_id: str) -> None:
        """
        Deleta um link de pagamento
        
        Args:
            link_id: ID do link de pagamento
        """
        if not link_id:
            raise ValueError("ID é obrigatório")
        
        self.http.delete(f"/payment-links/{link_id}")
    
    def get_checkout_url(self, slug: str, base_url: Optional[str] = None) -> str:
        """
        Obtém a URL pública do checkout.

        Observação: o objeto retornado por ``create()``/``get()`` já inclui o
        campo ``url``. Use este helper apenas se precisar montar a URL a partir do slug.

        Args:
            slug: Slug do link de pagamento
            base_url: URL base do checkout (padrão: https://checkout.usealpa.com/pay)

        Returns:
            URL completa do checkout
        """
        checkout_base = base_url or "https://checkout.usealpa.com/pay"
        return f"{checkout_base}/{slug}"
