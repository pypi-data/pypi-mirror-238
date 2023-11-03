# Payze Uzbekistan implementation.

Support Group - <a href="https://t.me/+Ng1axYLNyBAyYTRi">Telegram</a> <br/>

## Installation

```shell
pip install payze-pkg
```

### Test-Credentials

```
Card Numer: 8600 0000 000 00007 Expire Date: 04/26
Card Numer: 9860 00000 0000 000 Expire Date: 04/26
```

## Account2Card Documentation
- [AddCard](#addcard)
- [VerifyCard](#verifycard)
- [Account2Card](#account2card)
- [StatusCheck](#statuscheck)

# Methods

## AddCard

```python
from payze.types.params import AddCardDataParam
from payze.clinet.account2card import PayzeAccount2CardAPI


account2card = PayzeAccount2CardAPI(
    key="your-key",
    secret="your-secret",
    url="payze-url",
    url_mobile_cards="payze-mobile-cards",
    web_hook_gateway="your-webhook-gateway",
    error_redirect_gateway="your-error-redirect-gateway",
    success_redirect_gateway="your-success-redirect-gateway"
)

resp_obj = account2card.add_card(
    params=AddCardDataParam(
        source="Card",
        amount=1,
        currency="USD",
        language="EN",
        tokenize_card=True
    )
)

print(resp_obj)
```

## VerifyCard

```python
from payze.types.params import VerifyCardDataParam
from payze.clinet.account2card import PayzeAccount2CardAPI


account2card = PayzeAccount2CardAPI(
    key="your-key",
    secret="your-secret",
    url="payze-url",
    url_mobile_cards="payze-mobile-cards",
    web_hook_gateway="your-webhook-gateway",
    error_redirect_gateway="your-error-redirect-gateway",
    success_redirect_gateway="your-success-redirect-gateway"
)

resp_obj = account2card_client.verify_card(
    params=VerifyCardDataParam(
        number="8600000000000007",
        card_holder="xxx",
        expire_date="04/26",
        transaction_id="trx-id" # your can get transaction-id from add card method
    )
)
print(resp_obj)
```

## Account2Card

```python
from payze.types.params import RefundParam
from payze.types.params import ExtraAttribute
from payze.clinet.account2card import PayzeAccount2CardAPI


account2card = PayzeAccount2CardAPI(
    key="your-key",
    secret="your-secret",
    url="payze-url",
    url_mobile_cards="payze-mobile-cards",
    web_hook_gateway="your-webhook-gateway",
    error_redirect_gateway="your-error-redirect-gateway",
    success_redirect_gateway="your-success-redirect-gateway"
)

resp_obj = account2card_client.account2card(
    params=RefundParam(
        source="Wallet",
        amount=1,
        currency="UZS",
        language="EN",
        token="card-token",
        extra_attributes=[
            ExtraAttribute(
                key="order_id",
                value="1721",
                description="it's order"
            ).to_dict()
        ]
    )
)
print(resp_obj)
```

## StatusCheck

```python
from payze.types.params import StatusCheckParam
from payze.clinet.account2card import PayzeAccount2CardAPI


account2card = PayzeAccount2CardAPI(
    key="your-key",
    secret="your-secret",
    url="payze-url",
    url_mobile_cards="payze-mobile-cards",
    web_hook_gateway="your-webhook-gateway",
    error_redirect_gateway="your-error-redirect-gateway",
    success_redirect_gateway="your-success-redirect-gateway"
)

resp_obj = account2card_client.status_check(
    params=StatusCheckParam(
        check_id="check-id" # you can use transaction-id
    )
)
print(resp_obj)
```
