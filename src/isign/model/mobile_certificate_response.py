from .certificate import Certificate
from .response import Response


class MobileCertificateResponse(Response):
    @property
    def signing_certificate(self) -> Certificate:
        return Certificate(self.raw["signing_certificate"])

    @property
    def authentication_certificate(self) -> Certificate:
        return Certificate(self.raw["authentication_certificate"])

    @property
    def country(self) -> str:
        return str(self.raw["country"])

    @property
    def code(self) -> str:
        return str(self.raw["code"])

    @property
    def name(self) -> str:
        return str(self.raw["name"])

    @property
    def surname(self) -> str:
        return str(self.raw["surname"])
