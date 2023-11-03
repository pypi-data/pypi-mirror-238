"""
the payze responses.
"""
from typing import Any
from typing import List
from typing import Optional

from pydantic import Field
from pydantic import BaseModel


class CardPayment(BaseModel):
    """
    the card payment response.
    """
    token: str
    preauthorize: bool
    rrn: Optional[str]
    google_pay: bool = Field(alias="googlePay")
    apple_pay: bool = Field(alias="applePay")
    card_mask: Optional[str] = Field(alias="cardMask")
    card_expiration: Optional[str] = Field(alias="cardExpiration")
    merchant_id: Optional[str] = Field(alias="merchantId")
    terminal_id: Optional[str] = Field(alias="terminalId")
    processing_vendor_id: Optional[str] = Field(alias="processingVendorId")
    processing_vendor: Optional[str] = Field(alias="processingVendor")


class WalletPayment(BaseModel):
    """
    the wallet payment response.
    """
    flow: str
    token: str
    tokenize_card: Optional[bool] = Field(alias="tokenizeCard")


class Hooks(BaseModel):
    """
    the hooks response.
    """
    webhook_gateway: str = Field(alias="webhookGateway")
    success_redirect_gateway: str = Field(alias="successRedirectGateway")
    error_redirect_gateway: str = Field(alias="errorRedirectGateway")


class Payer(BaseModel):
    """
    the payer response.
    """
    ip: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    country: Optional[str]
    taxId: Optional[str] = Field(alias="taxId")
    fullName: Optional[str] = Field(alias="fullName")
    personalId: Optional[str] = Field(alias="personalId")


class ExtraAttributes(BaseModel):
    """
    extra attributes
    """
    key: str
    value: str
    description: str


class Metadata(BaseModel):
    """
    metadata
    """
    extra_attributes: Optional[List[ExtraAttributes]] = \
        Field(alias="extraAttributes")


class Payment(BaseModel):
    """
    the payment response
    """
    id: int
    type: str
    source: str
    amount: float
    currency: str
    status: str
    hooks: Hooks
    language: str
    network: Optional[str]
    settled: Optional[dict]
    fee: Optional[Any]
    channel: Optional[dict]
    payer: Optional[Payer]
    receipt: Optional[dict]

    payment_url: Optional[str] = Field(
        alias="paymentUrl"
    )
    rejected_date: Optional[str] = Field(
        alias="rejectedDate"
    )
    reverse_date: Optional[str] = Field(
        alias="reverseDate"
    )
    refunded_date: Optional[str] = Field(
        alias="refundedDate"
    )
    settled_date: Optional[str] = Field(
        alias="settledDate"
    )
    blocked_date: Optional[str] = Field(
        alias="blockedDate"
    )
    captured_date: Optional[str] = Field(
        alias="capturedDate"
    )
    reject_reason: Optional[str] = Field(
        alias="rejectReason"
    )
    requester_id: int = Field(
        alias="requesterId"
    )
    transaction_id: str = Field(
        alias="transactionId"
    )
    sand_box: bool = Field(
        alias="sandBox"
    )
    created_date: str = Field(
        alias="createdDate"
    )
    idempotency_key: Optional[str] = Field(
        alias="idempotencyKey"
    )
    share_link: Optional[str] = Field(
        alias="shareLink"
    )
    card_payment: CardPayment = Field(
        alias="cardPayment"
    )
    wallet_payment: WalletPayment = Field(
        alias="walletPayment"
    )
    blocked_amount: Optional[float] = Field(
        alias="blockedAmount"
    )
    captured_amount: Optional[float] = Field(
        alias="capturedAmount"
    )
    refunded_amount: Optional[float] = Field(
        alias="refundedAmount"
    )
    reversed_amount: Optional[float] = Field(
        alias="reversedAmount"
    )
    settled_balance_amount: Optional[float] = Field(
        alias="settledBalanceAmount"
    )
    cross_currency_settlement: Optional[dict] = Field(
        alias="crossCurrencySettlement"
    )
    metadata: Optional[Metadata] = Field(alias="metadata")


class Data(BaseModel):
    """
    the payment data response
    """
    payment: Payment


class ValueData(Payment):
    """
    the value data response
    """


class Status(BaseModel):
    """
    the status response
    """
    message: Optional[str]
    errors: Optional[dict]
    type: Optional[str]


class ResponseAddCard(BaseModel):
    """
    the add card response.
    """
    data: Data
    status: Status


class ResponseVerifyCard(BaseModel):
    """
    the response verify card.
    """
    success: bool


class ResponseRefund(BaseModel):
    """
    the response refund.
    """
    data: Data
    status: Status


class PaymentHistory(BaseModel):
    """
    the payment history response.
    """
    value: List[ValueData]
    count: Optional[int]


class ResponseStatusCheck(BaseModel):
    """
    the response status check.
    """
    status: Status
    data: PaymentHistory
