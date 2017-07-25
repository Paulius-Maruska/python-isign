from typing import List, Optional, Tuple, Union

from .base import BaseDict
from .file import File, Files, files as files_func


class PDF(BaseDict):
    @property
    def contact(self) -> str:
        return str(self.raw["contact"])

    @contact.setter
    def contact(self, value: str) -> None:
        self.raw["contact"] = value

    @property
    def location(self) -> str:
        return str(self.raw["location"])

    @location.setter
    def location(self, value: str) -> None:
        self.raw["location"] = value

    @property
    def signing_purpose(self) -> str:
        return str(self.raw.get("signing_purpose", "signature"))

    @signing_purpose.setter
    def signing_purpose(self, value: str) -> None:
        if value not in ("registration", "signature"):
            raise ValueError("signing_purpose can be set to 'registration' or 'signature'.")
        self.raw["signing_purpose"] = value

    @property
    def reason(self) -> str:
        return str(self.raw.get("reason", ""))

    @reason.setter
    def reason(self, value: str) -> None:
        self.raw["reason"] = value

    @property
    def files(self) -> Files:
        if "files" not in self.raw:
            self.raw["files"] = []
        return Files(self.raw["files"])


def pdf(contact: str, location: str,
        signing_purpose: Optional[str] = None,
        reason: Optional[str] = None,
        files: Optional[Union[Files, List[Union[File, Tuple[str, str, str]]]]] = None) -> PDF:
    raw = {
        "contact": contact,
        "location": location,
        "files": [],
    }
    if signing_purpose is not None:
        raw["signing_purpose"] = signing_purpose
    if reason is not None:
        raw["reason"] = reason
    if files is not None:
        if isinstance(files, Files):
            raw["files"] = files.raw
        elif isinstance(files, list):
            raw["files"] = files_func(*files).raw
        else:
            raise ValueError("files must be an instance of class Files or a list of arguments for files function.")
    return PDF(raw)
