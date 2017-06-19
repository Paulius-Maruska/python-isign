from base64 import b64decode
from datetime import datetime

from dateutil.parser import parse


class DateTimeStr(str):
    def as_datetime(self) -> datetime:
        return parse(self)


class Base64Str(str):
    def as_bytes(self) -> bytes:
        return b64decode(self)

    def as_str(self) -> str:
        return self.as_bytes().decode("utf-8")
