"""
custom exceptions.
"""


class BaseError(Exception):
    """
    Base error superclass.
    """
    def __init__(self, message="Payze exception"):
        super().__init__(message)


class PayzeServiceException(BaseError):
    """
    PayzeServiceException
    """


class GetCardTransactionIDException(BaseError):
    """
    GetCardTransactionIDException
    """


class BindTokenException(BaseError):
    """
    BindTokenException
    """


class Account2CardException(BaseError):
    """
    Account2CardException
    """


class GetDriverCardInfodException(BaseError):
    """
    GetDriverCardInfodException
    """


class NotImplementException(BaseError):
    """
    NotImplementException
    """
