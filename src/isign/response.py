from typing import Dict


class Response:
    def __init__(self, content: Dict) -> None:
        self.content = content

    @property
    def status(self) -> str:
        return str(self.content["status"])
