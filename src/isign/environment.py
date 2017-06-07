from typing import Dict
from urllib.parse import (
    urlencode,
    urlunsplit,
)


class ISignEnvironment:
    def __init__(self, name: str, netloc: str, scheme: str = "https") -> None:
        self.name = name
        self.netloc = netloc
        self.scheme = scheme

    def __repr__(self) -> str:
        return f"ISignEnvironment(name={self.name!r}, netloc={self.netloc!r}, scheme={self.scheme!r})"

    def __str__(self) -> str:
        return f"< isign env {self.name!r} {self.netloc} >"

    def construct_url(self, access_token: str, path: str) -> str:
        if not access_token:
            raise ValueError("access_token must be provided")
        query = urlencode({"access_token": access_token})
        components = self.scheme, self.netloc, path, query, ""
        return urlunsplit(components)


SANDBOX = ISignEnvironment("sandbox", "developers.isign.io")
LIVE = ISignEnvironment("live", "api2.isign.io")
ENV_MAP: Dict[str, ISignEnvironment] = {
    SANDBOX.name: SANDBOX,
    LIVE.name: LIVE,
}


def get_default_environment(name: str) -> ISignEnvironment:
    if name not in ENV_MAP:
        raise ValueError(f"unknown ISignEnvironment {name!r}")
    return ENV_MAP[name]
