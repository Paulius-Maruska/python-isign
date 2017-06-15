from typing import Sequence

from .base import Base
from .error_field import ErrorField


class Error(Base):
    @property
    def status(self) -> str:
        return str(self.raw["status"])

    @property
    def error_code(self) -> int:
        return int(self.raw["error_code"])

    @property
    def message(self) -> str:
        return str(self.raw["message"])

    @property
    def errors(self) -> Sequence[ErrorField]:
        errors = self.raw.get("errors", None)
        if not errors:
            return []
        return [ErrorField(err) for err in errors]

    def __str__(self) -> str:
        result = f"{self.message} ({self.error_code})"
        errors = "\n".join([f"  {err}" for err in self.errors])
        if errors:
            result += f":\n{errors}"
        return result
