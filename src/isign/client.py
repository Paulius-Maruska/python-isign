from typing import Optional

from .connection import ISignConnection
from .model import (
    MobileCertificateResponse,
    MobileLoginResponse,
    MobileLoginStatusResponse,
    MobileSignResponse,
    MobileSignStatusResponse,
    PDF,
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

    def mobile_sign(self, phone: str, code: str,
                    language: str, message: str,
                    type: str = "pdf",
                    timestamp: bool = True,
                    pdf: Optional[PDF] = None) -> MobileSignResponse:
        path = "/mobile/sign.json"
        payload = {
            "phone": phone,
            "code": code,
            "language": language,
            "message": message,
            "type": type,
            "timestamp": timestamp,
        }
        if type == "pdf":
            if pdf is None:
                raise ValueError("pdf argument must not be None, when type argument is 'pdf'")
            payload["pdf"] = pdf.raw
        else:
            raise ValueError("not supported type")

        data = self.connection.post(path, payload)
        return MobileSignResponse(data)

    def mobile_sign_status(self, token: str) -> MobileSignStatusResponse:
        path = f"/mobile/sign/status/{token}.json"
        data = self.connection.get(path)
        return MobileSignStatusResponse(data)
