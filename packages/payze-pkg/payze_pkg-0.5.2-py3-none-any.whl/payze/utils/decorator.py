"""
payze utilities.
"""
import logging
import requests

from payze.exceptions.service import PayzeServiceException


logger = logging.getLogger(__name__)


def error_catcher(func):
    """
    send request decorator
    for catching exceptions.
    """
    def wrapper(self, *args, **kwargs):
        response = None

        try:
            response = func(self, *args, **kwargs)
            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as exc:
            message = f"payze - error: {exc} args: {args} kwargs: {kwargs}" # noqa

            if response is not None:
                message += f" response: {response.text}"

            logger.error(message)
            raise PayzeServiceException(message) from exc

        except Exception as exc:
            message = f"exception: {exc} args: {args} kwargs: {kwargs}" # noqa

            if response is not None:
                message += f" response: {response.text}"

            logger.error(message)
            raise PayzeServiceException(message) from exc

    return wrapper
