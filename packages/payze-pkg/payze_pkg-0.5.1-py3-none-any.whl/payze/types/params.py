"""
payze param types for using payze client methods.
"""
from uuid import uuid4
from dataclasses import dataclass


@dataclass
class AddCardDataParam:
    """
    verifyCardData represents.
    """
    source: str
    amount: str
    currency: str
    language: str
    tokenize_card: bool
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
            "idempotencyKey": self.idempotency_key
        }


@dataclass
class VerifyCardDataParam:
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


@dataclass
class RefundParam:
    """
    RefundParam represents.
    """
    source: str
    amount: float
    currency: str
    language: str
    token: str
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
            "idempotencyKey": self.idempotency_key
        }


@dataclass
class StatusCheckParam:
    """
    RequestStatusCheck represents.
    """
    check_id: str
