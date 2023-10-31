"""
payze utilities.
"""
import logging
import requests

from ubk.types.http.rpc_error import JsonRPCError
from ubk.types.http.rpc_response import JsonRPCResponse
from ubk.exceptions.service import UBKServiceException


logger = logging.getLogger(__name__)


def send_request(func):
    """
    send request decorator
    for catching exceptions.
    """
    def wrapper(self, *args, **kwargs):
        response: dict = None
        try:
            response = func(self, *args, **kwargs)
            response.raise_for_status()
            resp_json = response.json()

            resp_err = JsonRPCError(**resp_json)

            if resp_err.error is not None:
                raise UBKServiceException(
                    message=f"{resp_err.error}"
                )

            return JsonRPCResponse(**resp_json)

        except (requests.exceptions.RequestException, UBKServiceException) as exc: # noqa
            message = f"ubk - error: {exc} args: {args} kwargs: {kwargs}" # noqa

            if response is not None:
                message += f" response: {response}"

            logger.error(message)
            raise UBKServiceException(exc) from exc

    return wrapper
