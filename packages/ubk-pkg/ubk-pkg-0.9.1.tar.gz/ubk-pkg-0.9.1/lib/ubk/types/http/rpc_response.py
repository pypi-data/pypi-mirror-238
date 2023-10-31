"""
response.
"""
from typing import List
from pydantic import BaseModel


class Title(BaseModel):
    """
    the title.
    """
    ru: str
    en: str
    uz: str


class Account(BaseModel):
    """
    the account.
    """
    name: str
    title: Title
    mask: str = ''
    number: str = ''
    value: str = None


class Payment(BaseModel):
    """
    the payment.
    """
    ref_num: str


class Merchant(BaseModel):
    """
    the merchant.
    """
    organization: str
    epos: dict
    type: Title


class Result(BaseModel):
    """
    the result.
    """
    ext_id: str
    state: int
    number: str
    description: str
    amount: int
    currency: str
    commission: float
    account: List[Account]
    payment: Payment
    merchant: Merchant


class Host(BaseModel):
    """
    the host.
    """
    host: str
    timestamp: str


class JsonRPCResponse(BaseModel):
    """
    the json rpc response
    """
    jsonrpc: str
    result: Result
    id: str
    status: bool
    origin: str
    host: Host
