from typing import Any, Dict, List, Optional, Sized


class BaseDict(Sized):
    def __init__(self, raw: Optional[Dict[str, Any]] = None) -> None:
        self.raw: Dict[str, Any] = {}
        if raw is not None:
            self.raw = raw

    def __len__(self) -> int:
        return len(self.raw)


class BaseList(Sized):
    def __init__(self, raw: Optional[List[Any]] = None) -> None:
        self.raw: List[Any] = []
        if raw is not None:
            self.raw = raw

    def __len__(self) -> int:
        return len(self.raw)
