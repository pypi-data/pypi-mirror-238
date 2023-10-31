"""
request body
"""
from uuid import uuid4

from typing import Any

from pydantic import BaseModel


class Base(BaseModel):
    """
    the base model.
    """
    ext_id: str


class Create(Base):
    """
    the transfer credit create
    """
    number: str
    amount: int
    ext_id: str = str(uuid4())


class Confirm(Base):
    """
    the transfer credit confirm
    """
    ext_id: str


class Cancel(Base):
    """
    the transfer credit cancel
    """


class State(Base):
    """
    the transfer credit state
    """


class Account2Card(Create):
    """
    the account2card pay
    """


class JsonRpcRequest(BaseModel):
    """
    the json rpc request.
    """
    method: str
    params: Any
    id: str = str(uuid4())
    jsonrpc: str = "2.0"
