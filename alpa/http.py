"""
Cliente HTTP base para requisições
"""

import json
from typing import Any, Dict, Optional
from urllib.parse import urlencode
import requests
from .utils.errors import handle_api_error


class HttpClient:
    """Cliente HTTP para fazer requisições à API"""
    
    def __init__(
        self,
        api_key: str,
        base_url: str,
        version: str = "v1",
        timeout: int = 30
    ):
        """
        Inicializa o cliente HTTP
        
        Args:
            api_key: API key da Alpa
            base_url: URL base da API
            version: Versão da API
            timeout: Timeout das requisições em segundos
        """
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.version = version
        self.timeout = timeout
        
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',
            'User-Agent': 'Alpa-Python-SDK/2.0.0'
        })
    
    def request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None
    ) -> Any:
        """
        Faz uma requisição HTTP
        
        Args:
            method: Método HTTP (GET, POST, PATCH, DELETE)
            endpoint: Endpoint da API
            data: Dados para enviar no body
            params: Parâmetros de query
            
        Returns:
            Resposta da API parseada
            
        Raises:
            AlpaError: Se houver erro na requisição
        """
        url = f"{self.base_url}/api/{self.version}{endpoint}"
        
        # Adiciona query params
        if params:
            # Remove valores None
            clean_params = {k: v for k, v in params.items() if v is not None}
            if clean_params:
                url += f"?{urlencode(clean_params)}"
        
        try:
            response = self.session.request(
                method=method,
                url=url,
                json=data,
                timeout=self.timeout
            )
            
            # Parse da resposta
            try:
                body = response.json()
            except ValueError:
                body = response.text
            
            # Verifica se houve erro
            if not response.ok:
                raise handle_api_error(response, body)

            # Desempacota o envelope padrão: { success: true, data: X, pagination?: Y }
            if isinstance(body, dict) and body.get('success') is True and 'data' in body:
                if 'pagination' in body:
                    return {'data': body['data'], 'pagination': body['pagination']}
                if 'meta' in body:
                    return {'data': body['data'], 'meta': body['meta']}
                return body['data']

            return body
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Erro na requisição: {str(e)}")
    
    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Any:
        """Faz uma requisição GET"""
        return self.request('GET', endpoint, params=params)
    
    def post(self, endpoint: str, data: Optional[Dict[str, Any]] = None) -> Any:
        """Faz uma requisição POST"""
        return self.request('POST', endpoint, data=data)
    
    def patch(self, endpoint: str, data: Optional[Dict[str, Any]] = None) -> Any:
        """Faz uma requisição PATCH"""
        return self.request('PATCH', endpoint, data=data)
    
    def delete(self, endpoint: str) -> Any:
        """Faz uma requisição DELETE"""
        return self.request('DELETE', endpoint)
