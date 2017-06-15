from typing import Dict


class Base:
    def __init__(self, raw: Dict) -> None:
        self.raw = raw

    @property
    def status(self) -> str:
        return str(self.raw["status"])
