"""
Recurso de Clientes
"""

import re
from typing import Optional, Dict, Any
from ..http import HttpClient


class ClientsResource:
    """Recurso para gerenciar Clientes"""
    
    def __init__(self, http: HttpClient):
        self.http = http
    
    def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Cria um novo cliente
        
        Args:
            data: Dados do cliente
                - name: Nome do cliente (obrigatório)
                - email: Email do cliente (obrigatório, válido)
                - document: CPF/CNPJ
                - phone: Telefone
                
        Returns:
            Cliente criado
        """
        # Validação básica
        if not data.get("name") or len(str(data["name"]).strip()) == 0:
            raise ValueError("Nome do cliente é obrigatório")
        
        if not data.get("email") or not self._is_valid_email(data["email"]):
            raise ValueError("Email inválido")
        
        return self.http.post("/clients", data)
    
    def list(
        self,
        page: Optional[int] = None,
        limit: Optional[int] = None,
        cursor: Optional[str] = None,
        order_by: Optional[str] = None,
        order_direction: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Lista clientes
        
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
        
        response = self.http.get("/clients", params)
        
        # Mapear resposta: { message, clients, pagination } -> { data, pagination }
        return {
            "data": response.get("clients") or response.get("data") or [],
            "pagination": response.get("pagination") or {"total": 0, "page": 1, "limit": 10}
        }
    
    def get(self, client_id: str) -> Dict[str, Any]:
        """
        Obtém um cliente por ID
        
        Args:
            client_id: ID do cliente
            
        Returns:
            Cliente
        """
        if not client_id:
            raise ValueError("ID é obrigatório")
        
        return self.http.get(f"/clients/{client_id}")
    
    def update(self, client_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Atualiza um cliente
        
        Args:
            client_id: ID do cliente
            data: Dados para atualizar
            
        Returns:
            Cliente atualizado
        """
        if not client_id:
            raise ValueError("ID é obrigatório")
        
        if data.get("email") and not self._is_valid_email(data["email"]):
            raise ValueError("Email inválido")
        
        return self.http.patch(f"/clients/{client_id}", data)
    
    def _is_valid_email(self, email: str) -> bool:
        """Valida formato de email"""
        pattern = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
        return bool(re.match(pattern, email))
