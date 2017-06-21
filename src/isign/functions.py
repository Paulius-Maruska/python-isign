from typing import Optional, Union

from .client import ISignClient
from .connection import ISignConnection
from .environment import ISignEnvironment
from .model import (
    MobileCertificateResponse,
    MobileLoginResponse,
    MobileLoginStatusResponse,
)

ISIGN_ENVIRONMENT: Union[str, ISignEnvironment] = "sandbox"
ISIGN_ACCESS_TOKEN: Optional[str] = None
ISIGN_USER_AGENT: str = "python-isign"


def use_config(access_token: str,
               user_agent: Optional[str] = None,
               environment: Optional[Union[str, ISignEnvironment]] = None
               ) -> None:
    global ISIGN_ENVIRONMENT, ISIGN_ACCESS_TOKEN, ISIGN_USER_AGENT
    ISIGN_ACCESS_TOKEN = access_token
    if isinstance(user_agent, str):
        ISIGN_USER_AGENT = user_agent
    if isinstance(environment, (str, ISignEnvironment)):
        ISIGN_ENVIRONMENT = environment


def global_client() -> ISignClient:
    if not isinstance(ISIGN_ACCESS_TOKEN, str):
        raise ValueError("ISIGN_ACCESS_TOKEN is not set or is incorrect. Call use_config function to set it.")
    if not isinstance(ISIGN_USER_AGENT, str):
        raise ValueError("ISIGN_USER_AGENT is not set or is incorrect. Call use_config function to set it.")
    if not isinstance(ISIGN_ENVIRONMENT, (str, ISignEnvironment)):
        raise ValueError("ISIGN_ENVIRONMENT is not set or is incorrect. Call use_config function to set it.")
    environment = ISIGN_ENVIRONMENT
    connection = ISignConnection(ISIGN_ACCESS_TOKEN, ISIGN_USER_AGENT, environment)
    return ISignClient(connection)


def mobile_certificate(phone: str,
                       code: str
                       ) -> MobileCertificateResponse:
    client = global_client()
    return client.mobile_certificate(phone, code)


def mobile_login(phone: str,
                 code: str,
                 language: Optional[str] = None,
                 message: Optional[str] = None
                 ) -> MobileLoginResponse:
    client = global_client()
    return client.mobile_login(phone, code, language, message)


def mobile_login_status(token: str) -> MobileLoginStatusResponse:
    client = global_client()
    return client.mobile_login_status(token)
