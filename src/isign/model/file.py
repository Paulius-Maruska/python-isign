from typing import Tuple, Union

from .base import BaseDict, BaseList


class File(BaseDict):
    @property
    def name(self) -> str:
        return str(self.raw["name"])

    @property
    def digest(self) -> str:
        return str(self.raw["digest"])

    @property
    def content(self) -> str:
        return str(self.raw["content"])


class Files(BaseList):
    def __getitem__(self, key: int) -> File:
        return File(self.raw[key])

    def __setitem__(self, key: int, value: File) -> None:
        self.raw[key] = value.raw

    def __delitem__(self, key: int) -> None:
        del self.raw[key]

    def append(self, value: File) -> None:
        self.raw.append(value.raw)


def file(name: str, digest: str, content: str) -> File:
    return File({"name": name, "digest": digest, "content": content})


def files(*args: Union[File, Tuple[str, str, str]]) -> Files:
    f = Files()
    for arg in args:
        if isinstance(arg, File):
            f.append(arg)
        elif isinstance(arg, tuple) and len(arg) == 3:
            f.append(file(*arg))
        else:
            raise ValueError("arguments for files function must be either instances of File or tuples of 3 strings.")
    return f
