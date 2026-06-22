"""
Classes de erro customizadas para o SDK
"""

from typing import Any, Optional


class AlpaError(Exception):
    """Erro base do SDK Alpa"""

    def __init__(
        self,
        message: str,
        code: Optional[str] = None,
        status: Optional[int] = None,
        details: Optional[Any] = None
    ):
        super().__init__(message)
        self.message = message
        self.code = code
        self.status = status
        self.status_code = status
        self.details = details


class AlpaAuthenticationError(AlpaError):
    """Erro de autenticação"""

    def __init__(self, message: str = "Falha na autenticação. Verifique sua API key."):
        super().__init__(message, "AUTHENTICATION_ERROR", 401)


class AlpaValidationError(AlpaError):
    """Erro de validação"""

    def __init__(self, message: str, details: Optional[Any] = None):
        super().__init__(message, "VALIDATION_ERROR", 400, details)


class AlpaNotFoundError(AlpaError):
    """Recurso não encontrado"""

    def __init__(self, resource: str, resource_id: Optional[str] = None):
        message = f"{resource} com ID {resource_id} não encontrado." if resource_id else f"{resource} não encontrado."
        super().__init__(message, "NOT_FOUND", 404)


class AlpaRateLimitError(AlpaError):
    """Erro de limite de requisições"""

    def __init__(self, message: str = "Limite de requisições excedido. Tente novamente mais tarde."):
        super().__init__(message, "RATE_LIMIT_ERROR", 429)


class AlpaServerError(AlpaError):
    """Erro do servidor"""

    def __init__(self, message: str = "Erro interno do servidor. Tente novamente mais tarde."):
        super().__init__(message, "SERVER_ERROR", 500)


def handle_api_error(response, body: Optional[Any] = None) -> AlpaError:
    """
    Converte erros HTTP em erros do SDK

    Args:
        response: Objeto Response do requests
        body: Corpo da resposta parseado

    Returns:
        Erro apropriado do SDK
    """
    status = response.status_code
    message = body.get("message") if isinstance(body, dict) else f"HTTP {status}: {response.reason}"
    code = body.get("code") if isinstance(body, dict) else None

    if status == 401:
        return AlpaAuthenticationError(message)
    elif status == 400:
        details = body.get("details") if isinstance(body, dict) else None
        return AlpaValidationError(message, details)
    elif status == 404:
        resource_id = body.get("id") if isinstance(body, dict) else None
        return AlpaNotFoundError("Recurso", resource_id)
    elif status == 429:
        return AlpaRateLimitError(message)
    elif status in [500, 502, 503]:
        return AlpaServerError(message)
    else:
        return AlpaError(message, code, status, body)
