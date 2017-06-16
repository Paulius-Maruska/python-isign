from typing import Dict


class FieldError:
    def __init__(self, raw: Dict) -> None:
        self.raw = raw

    @property
    def error_code(self) -> int:
        return int(self.raw["error_code"])

    @property
    def message(self) -> str:
        return str(self.raw["message"])

    @property
    def field(self) -> str:
        return str(self.raw["field"])

    def __str__(self) -> str:
        return f"{self.field} - {self.message} ({self.error_code})"
