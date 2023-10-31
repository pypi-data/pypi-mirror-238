"""
the base client for UniPostApi
"""
import logging

from requests import request

from ubk.types.http import rpc_request
from ubk.utils.decorator import send_request
from ubk.types.http.rpc_request import JsonRpcRequest
from ubk.types.http.rpc_response import JsonRPCResponse


logger = logging.getLogger(__name__)


class UniPosAPI:
    """
    the default UniPoApi
    """
    def __init__(
        self,
        url: str,
        token: str,
    ):
        self.url = url
        self.access_token = token
        self.timeout = 20
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.access_token}'
        }
        self.methods = {
            "create_check": "transfer.credit.create",
            "pay_check": "transfer.credit.confirm",
            "status_check": "transfer.credit.state",
            "cancel_check": "transfer.credit.cancel"
        }

    @send_request
    def __send_request(self, method, params=None):
        """
        do request.
        """
        data = JsonRpcRequest(
            method=method,
            params=params
        )

        return request(
            method="POST",
            url=self.url,
            data=data.model_dump_json(),
            headers=self.headers,
            timeout=self.timeout
        )

    def _create_check(self, params: rpc_request.Create) -> JsonRPCResponse:
        """
        implementation of create_check.
        """
        method = self.methods.get("create_check")

        return self.__send_request(method, params)

    def _pay_check(self, params: rpc_request.Confirm) -> JsonRPCResponse:
        """
        implementation of pay_check.
        """
        method = self.methods.get("pay_check")

        return self.__send_request(method, params)

    def account2card(self, params: rpc_request.Account2Card) -> JsonRPCResponse: # noqa
        """
        implementation of account2card.
        """
        # create check
        resp_create_check = self._create_check(
            params=rpc_request.Create(
                number=params.number,
                amount=params.amount,
                ext_id=params.ext_id
            )
        )

        # pay check
        return self._pay_check(
            params=rpc_request.Confirm(
                ext_id=resp_create_check.result.ext_id
            )
        )

    def status_check(self, params: rpc_request.State) -> JsonRPCResponse:
        """
        implementation of status_check.
        """
        method = self.methods.get("status_check")

        return self.__send_request(method, params)

    def cancel_check(self, params: rpc_request.Cancel) -> JsonRPCResponse:
        """
        implementation of status_check.
        """
        method = self.methods.get("cancel_check")

        return self.__send_request(method, params)
