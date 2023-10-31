"""
jsonrpc error response
"""
from typing import Union
from pydantic import BaseModel


class ErrorMessage(BaseModel):
    """
    the error messages
    """
    uz: str
    ru: str
    en: str


class Error(BaseModel):
    """
    the error base response.
    """
    code: int
    message: Union[str, ErrorMessage]


class Host(BaseModel):
    """
    the host.
    """
    host: str
    timestamp: str


class JsonRPCError(BaseModel):
    """
    the json rpc error response.
    """
    jsonrpc: str
    id: str
    status: bool
    origin: str
    host: Host
    error: Error = None
