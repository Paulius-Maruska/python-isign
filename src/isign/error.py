from typing import Any, Dict

from .model import Error


class ISignError(Exception):
    def __init__(self, method: str, path: str, status_code: int, response: Dict[str, Any]) -> None:
        super(ISignError, self).__init__()
        self.method = method
        self.path = path
        self.status_code = status_code
        self.error = Error(response)

    def __str__(self) -> str:
        return f"ISignError: {self.method} {self.path} -> {self.status_code}: {self.error}"
