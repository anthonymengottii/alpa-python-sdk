"""
Cliente principal do SDK Alpa
"""

from typing import Optional, Union
from .http import HttpClient
from .resources.payment_links import PaymentLinksResource
from .resources.transactions import TransactionsResource
from .resources.products import ProductsResource
from .resources.clients import ClientsResource
from .resources.coupons import CouponsResource
from .resources.subscriptions import SubscriptionsResource
from .resources.checkouts import CheckoutsResource
from .resources.offers import OffersResource
from .resources.withdrawals import WithdrawalsResource
from .resources.wallet import WalletResource
from .utils.webhooks import verify_webhook_signature


class AlpaClient:
    """
    Cliente principal para interagir com a API Alpa

    Exemplo:
        >>> from alpa import AlpaClient
        >>>
        >>> alpa = AlpaClient(api_key="sua_api_key_aqui")
        >>>
        >>> # Criar um link de pagamento
        >>> payment_link = alpa.payment_links.create({
        ...     "title": "Produto Premium",
        ...     "amountCents": 9900,  # R$ 99,00 em centavos
        ... })
        >>> print(payment_link["url"])
        >>>
        >>> # Listar transações
        >>> transactions = alpa.transactions.list(page=1, limit=10)
    """

    def __init__(
        self,
        api_key: str,
        base_url: Optional[str] = None,
        version: str = "v1",
        timeout: int = 30
    ):
        """
        Inicializa o cliente Alpa

        Args:
            api_key: Sua API key da Alpa (obrigatório)
            base_url: URL base da API (padrão: https://alpa-sistema-api.onrender.com)
            version: Versão da API (padrão: v1)
            timeout: Timeout das requisições em segundos (padrão: 30)

        Raises:
            ValueError: Se api_key não for fornecida
        """
        if not api_key:
            raise ValueError("API Key é obrigatória")

        self._http = HttpClient(
            api_key=api_key,
            base_url=base_url or "https://alpa-sistema-api.onrender.com",
            version=version,
            timeout=timeout
        )

        # Inicializa recursos
        self.payment_links = PaymentLinksResource(self._http)
        self.transactions = TransactionsResource(self._http)
        self.products = ProductsResource(self._http)
        self.clients = ClientsResource(self._http)
        self.coupons = CouponsResource(self._http)
        self.subscriptions = SubscriptionsResource(self._http)
        self.checkouts = CheckoutsResource(self._http)
        self.offers = OffersResource(self._http)
        self.withdrawals = WithdrawalsResource(self._http)
        self.wallet = WalletResource(self._http)

    def verify_webhook_signature(
        self,
        payload: Union[bytes, str],
        signature: str,
        secret: str
    ) -> bool:
        """
        Verifica a assinatura de um webhook (HMAC-SHA256 hex).

        Args:
            payload: Corpo bruto da requisição (bytes ou string)
            signature: Assinatura recebida no header X-Webhook-Signature
            secret: Secret da assinatura de webhook

        Returns:
            True se a assinatura for válida

        Exemplo:
            >>> import flask
            >>>
            >>> @app.route('/webhook', methods=['POST'])
            >>> def webhook():
            ...     payload = flask.request.data
            ...     signature = flask.request.headers.get('x-webhook-signature')
            ...
            ...     if alpa.verify_webhook_signature(payload, signature, webhook_secret):
            ...         # Processar webhook
            ...         pass
        """
        return verify_webhook_signature(payload, signature, secret)
