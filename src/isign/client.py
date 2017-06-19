from .connection import ISignConnection
from .model import MobileCertificateResponse


class ISignClient:
    def __init__(self, connection: ISignConnection) -> None:
        self.connection = connection

    def mobile_certificate(self, phone: str, code: str) -> MobileCertificateResponse:
        path = "/mobile/certificate.json"
        data = self.connection.post(path, {"phone": phone, "code": code})
        return MobileCertificateResponse(data)
