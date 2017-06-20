from typing import Optional

from .connection import ISignConnection
from .model import (
    MobileCertificateResponse,
    MobileLoginResponse,
    MobileLoginStatusResponse,
)


class ISignClient:
    def __init__(self, connection: ISignConnection) -> None:
        self.connection = connection

    def mobile_certificate(self, phone: str, code: str) -> MobileCertificateResponse:
        path = "/mobile/certificate.json"
        payload = {"phone": phone, "code": code}
        data = self.connection.post(path, payload)
        return MobileCertificateResponse(data)

    def mobile_login(self, phone: str, code: str,
                     language: Optional[str] = None,
                     message: Optional[str] = None) -> MobileLoginResponse:
        path = "/mobile/login.json"
        payload = {
            "phone": phone,
            "code": code,
        }
        if language:
            payload["language"] = language
        if message:
            payload["message"] = message
        data = self.connection.post(path, payload)
        return MobileLoginResponse(data)

    def mobile_login_status(self, token: str) -> MobileLoginStatusResponse:
        path = f"/mobile/login/status/{token}.json"
        data = self.connection.get(path)
        return MobileLoginStatusResponse(data)
