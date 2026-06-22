"""
Recursos do SDK Alpa
"""

from .payment_links import PaymentLinksResource
from .transactions import TransactionsResource
from .products import ProductsResource
from .clients import ClientsResource
from .coupons import CouponsResource

__all__ = [
    'PaymentLinksResource',
    'TransactionsResource',
    'ProductsResource',
    'ClientsResource',
    'CouponsResource',
]
