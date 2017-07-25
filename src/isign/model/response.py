from typing import Any, Dict, Optional

from .base import BaseDict


class Response(BaseDict):
    def __init__(self, raw: Optional[Dict[str, Any]]) -> None:
        super().__init__(raw)

    @property
    def status(self) -> str:
        return str(self.raw["status"])
