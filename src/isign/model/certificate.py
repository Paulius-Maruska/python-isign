from typing import Any, Dict

from .parsed import Base64Str, DateTimeStr


class CertificateSubject:
    def __init__(self, raw: Dict[str, str]) -> None:
        self.raw = raw

    @property
    def country(self) -> str:
        return self.raw["country"]

    @property
    def organisation(self) -> str:
        return self.raw["organisation"]

    @property
    def organisation_unit(self) -> str:
        return self.raw["organisation_unit"]

    @property
    def common_name(self) -> str:
        return self.raw["common_name"]

    @property
    def name(self) -> str:
        return self.raw["name"]

    @property
    def surname(self) -> str:
        return self.raw["surname"]

    @property
    def serial_number(self) -> str:
        return self.raw["serial_number"]


class CertificateIssuer:
    def __init__(self, raw: Dict[str, str]) -> None:
        self.raw = raw

    @property
    def country(self) -> str:
        return self.raw["country"]

    @property
    def organisation(self) -> str:
        return self.raw["organisation"]

    @property
    def common_name(self) -> str:
        return self.raw["common_name"]

    @property
    def email(self) -> str:
        return self.raw["email"]


class Certificate:
    def __init__(self, raw: Dict[str, Any]) -> None:
        self.raw = raw

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
