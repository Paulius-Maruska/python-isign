from .base import BaseDict
from .parsed import Base64Str, DateTimeStr


class CertificateSubject(BaseDict):
    @property
    def country(self) -> str:
        return str(self.raw["country"])

    @property
    def organisation(self) -> str:
        return str(self.raw["organisation"])

    @property
    def organisation_unit(self) -> str:
        return str(self.raw["organisation_unit"])

    @property
    def common_name(self) -> str:
        return str(self.raw["common_name"])

    @property
    def name(self) -> str:
        return str(self.raw["name"])

    @property
    def surname(self) -> str:
        return str(self.raw["surname"])

    @property
    def serial_number(self) -> str:
        return str(self.raw["serial_number"])


class CertificateIssuer(BaseDict):
    @property
    def country(self) -> str:
        return str(self.raw["country"])

    @property
    def organisation(self) -> str:
        return str(self.raw["organisation"])

    @property
    def common_name(self) -> str:
        return str(self.raw["common_name"])

    @property
    def email(self) -> str:
        return str(self.raw["email"])


class Certificate(BaseDict):
    @property
    def name(self) -> str:
        return str(self.raw["name"])

    @property
    def subject(self) -> CertificateSubject:
        return CertificateSubject(self.raw["subject"])

    @property
    def issuer(self) -> CertificateIssuer:
        return CertificateIssuer(self.raw["issuer"])

    @property
    def valid_from(self) -> DateTimeStr:
        return DateTimeStr(self.raw["valid_from"])

    @property
    def valid_to(self) -> DateTimeStr:
        return DateTimeStr(self.raw["valid_to"])

    @property
    def value(self) -> Base64Str:
        return Base64Str(self.raw["value"])
