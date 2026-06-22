"""
Recurso de Produtos
"""

from typing import Optional, Dict, Any
from ..http import HttpClient


class ProductsResource:
    """Recurso para gerenciar Produtos"""
    
    def __init__(self, http: HttpClient):
        self.http = http
    
    def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Cria um novo produto
        
        Args:
            data: Dados do produto
                - name: Nome do produto (obrigatório)
                - price: Preço em centavos (obrigatório, min 100)
                - description: Descrição do produto
                - imageUrl: URL da imagem
                - stockQuantity: Quantidade em estoque
                
        Returns:
            Produto criado
        """
        # Validação básica
        if not data.get("name") or len(str(data["name"]).strip()) == 0:
            raise ValueError("Nome do produto é obrigatório")
        
        if not data.get("price") or data.get("price", 0) < 100:
            raise ValueError("Preço mínimo é R$ 1,00 (100 centavos)")
        
        return self.http.post("/products", data)
    
    def list(
        self,
        page: Optional[int] = None,
        limit: Optional[int] = None,
        cursor: Optional[str] = None,
        order_by: Optional[str] = None,
        order_direction: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Lista produtos
        
        Args:
            page: Número da página
            limit: Limite de itens por página
            cursor: Cursor para paginação
            order_by: Campo para ordenação
            order_direction: Direção da ordenação (ASC ou DESC)
            
        Returns:
            Dicionário com 'data' (lista) e 'pagination'
        """
        params = {
            "page": page,
            "limit": limit,
            "cursor": cursor,
            "orderBy": order_by,
            "orderDirection": order_direction,
        }
        
        response = self.http.get("/products", params)
        return {
            "data": response.get("products") or response.get("data") or [],
            "pagination": response.get("pagination") or {"total": 0, "page": 1, "limit": 10},
        }
    
    def get(self, product_id: str) -> Dict[str, Any]:
        """
        Obtém um produto por ID
        
        Args:
            product_id: ID do produto
            
        Returns:
            Produto
        """
        if not product_id:
            raise ValueError("ID é obrigatório")
        
        return self.http.get(f"/products/{product_id}")
    
    def update(self, product_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Atualiza um produto
        
        Args:
            product_id: ID do produto
            data: Dados para atualizar
            
        Returns:
            Produto atualizado
        """
        if not product_id:
            raise ValueError("ID é obrigatório")
        
        if data.get("price") is not None and data.get("price", 0) < 100:
            raise ValueError("Preço mínimo é R$ 1,00 (100 centavos)")
        
        return self.http.patch(f"/products/{product_id}", data)
    
    def delete(self, product_id: str) -> None:
        """
        Deleta um produto
        
        Args:
            product_id: ID do produto
        """
        if not product_id:
            raise ValueError("ID é obrigatório")
        
        self.http.delete(f"/products/{product_id}")
