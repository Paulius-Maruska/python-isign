from .file import File
from .response import Response


class MobileSignResponse(Response):
    @property
    def token(self) -> str:
        return str(self.raw["token"])

    @property
    def control_code(self) -> str:
        return str(self.raw["control_code"])


class MobileSignStatusResponse(Response):
    @property
    def signature_id(self) -> str:
        return str(self.raw["signature_id"])

    @property
    def file(self) -> File:
        return File(self.raw["file"])
