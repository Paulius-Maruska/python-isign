from typing import Dict, Union

import requests

from .environment import (
    get_default_environment,
    ISignEnvironment,
)
from .error import ISignError


class ISignConnection:
    def __init__(self,
                 access_token: str,
                 user_agent: str = "Python iSign",
                 environment: Union[str, ISignEnvironment] = "sandbox"
                 ) -> None:
        self.access_token = access_token
        self.user_agent = user_agent
        if isinstance(environment, str):
            self.environment = get_default_environment(environment)
        elif isinstance(environment, ISignEnvironment):
            self.environment = environment
        else:
            raise ValueError("environment must be either str name or an instance of ISignEnvironment")

    def __repr__(self) -> str:
        return (f"ISignConnection("
                f"access_token={self.access_token!r}, "
                f"user_agent={self.user_agent!r}, "
                f"environment={self.environment!r})")

    def __str__(self) -> str:
        return f"< isign conn for {self.environment} >"

    def get(self, path: str) -> Dict:
        url = self.environment.construct_url(self.access_token, path)
        hdr = {"User-Agent": self.user_agent}
        response = requests.get(url, headers=hdr)
        if response.status_code >= 400:
            raise ISignError("GET", path, response.status_code, response.json())
        result: Dict = response.json()
        return result

    def post(self, path: str, content: Dict) -> Dict:
        url = self.environment.construct_url(self.access_token, path)
        hdr = {"User-Agent": self.user_agent}
        response = requests.post(url, headers=hdr, json=content)
        if response.status_code >= 400:
            raise ISignError("POST", path, response.status_code, response.json())
        result: Dict = response.json()
        return result
