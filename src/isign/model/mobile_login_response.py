from .certificate import Certificate
from .response import Response


class MobileLoginResponse(Response):
    @property
    def certificate(self) -> Certificate:
        return Certificate(self.raw["certificate"])

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

    @property
    def token(self) -> str:
        return str(self.raw["token"])

    @property
    def control_code(self) -> str:
        return str(self.raw["control_code"])


class MobileLoginStatusResponse(Response):
    pass
