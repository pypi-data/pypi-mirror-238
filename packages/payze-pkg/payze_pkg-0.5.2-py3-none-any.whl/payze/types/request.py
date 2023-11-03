"""
payze request types.
"""
from uuid import uuid4
from typing import List
from dataclasses import dataclass


@dataclass
class WalletPayment:
    """
    WalletPayment represents.
    """
    tokenize_card: bool = True

    def to_dict(self):
        """
        dict representation.
        """
        return {
            "tokenizeCard": self.tokenize_card
        }


@dataclass
class Hooks:
    """
    Web Hooks represents.
    """
    web_hook_gateway: str
    success_redirect_gateway: str
    error_redirect_gateway: str

    def to_dict(self):
        """
        dict representation.
        """
        return {
            "webhookGateway": self.web_hook_gateway,
            "successRedirectGateway": self.success_redirect_gateway,
            "errorRedirectGateway": self.error_redirect_gateway
        }


@dataclass
class RequestAddCardCreate:
    """
    Add Card Create represents.
    """
    hooks: Hooks
    wallet_payment: WalletPayment
    source: str
    amount: float
    currency: str
    language: str
    idempotency_key: str = str(uuid4())

    def to_dict(self):
        """
        dict representation.
        """
        return {
            "source": self.source,
            "amount": self.amount,
            "currency": self.currency,
            "language": self.language,
            "WalletPayment": {
                "tokenizeCard": self.wallet_payment.tokenize_card
            },
            "hooks": {
                "webhookGateway": self.hooks.web_hook_gateway,
                "successRedirectGateway": self.hooks.success_redirect_gateway, # noqa
                "errorRedirectGateway": self.hooks.error_redirect_gateway
            },
            "idempotencyKey": self.idempotency_key
        }


@dataclass
class RequestVerifyCardData:
    """
    CardData represents.
    """
    number: str
    card_holder: str
    expire_date: str
    transaction_id: str = None

    def to_dict(self):
        """
        dict representation.
        """
        return {
            "Number": self.number,
            "CardHolder": self.card_holder,
            "ExpirationDate": self.expire_date,
            "TransactionId": self.transaction_id
        }

    def to_form(self):
        """
        form representation.
        """
        return f"Number={self.number}&CardHolder={self.card_holder}&expirationDate={self.expire_date}&TransactionId={self.transaction_id}" # noqa


@dataclass
class ExtraAttribute:
    """
    extra attributes
    """
    key: str
    value: str
    description: str


@dataclass
class RequestRefund:
    """
    RequestRefund represents.
    """
    source: str
    amount: float
    currency: str
    language: str
    token: str
    hooks: Hooks
    idempotency_key: str = str(uuid4())
    extra_attributes: List[ExtraAttribute] = None

    def to_dict(self):
        """
        dict representation.
        """
        return {
            "source": self.source,
            "amount": self.amount,
            "currency": self.currency,
            "language": self.language,
            "token": self.token,
            "hooks": self.hooks.to_dict(),
            "idempotencyKey": self.idempotency_key,
            "Metadata": {
                "extraAttributes": self.extra_attributes,
            }
        }


@dataclass
class RequestStatusCheck:
    """
    RequestStatusCheck represents.
    """
    check_id: str

    def to_query_param(self) -> dict:
        """
        dict representation.
        """
        return {
            "$filter": f"transactionId eq '{self.check_id}'"
        }
