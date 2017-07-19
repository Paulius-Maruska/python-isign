from typing import Any, Dict, Optional


class Base:
    def __init__(self, raw: Optional[Dict[str, Any]] = None) -> None:
        self.raw: Dict[str, Any] = {}
        if raw:
            self.raw = raw
