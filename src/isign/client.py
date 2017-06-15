from isign.model import Response
from .connection import ISignConnection


class ISignClient:
    def __init__(self, connection: ISignConnection) -> None:
        self.connection = connection

    def mobile_certificate(self, phone: str, code: str) -> Response:
        path = "/mobile/certificate.json"
        data = self.connection.post(path, {"phone": phone, "code": code})
        return Response(data)
