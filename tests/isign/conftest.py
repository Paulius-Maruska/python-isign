import base64
import hashlib
import os
from typing import Optional, Tuple

import pytest
from _pytest.fixtures import SubRequest

import isign
from isign.environment import ISignEnvironment


@pytest.fixture(params=[("http", "foo"), ("https", "bar")], ids=["foo", "bar"])
def environment_params(request: SubRequest) -> Tuple[str, str, str]:
    scheme, name = request.param
    return name, "%s.isign.io" % name, scheme


@pytest.fixture()
def environment(environment_params: Tuple[str, str, str]) -> ISignEnvironment:
    name, netloc, scheme = environment_params
    return ISignEnvironment(name, netloc, scheme)


@pytest.fixture()
def sandbox_token() -> Optional[str]:
    import os
    token = os.environ.get("ISIGN_API_TOKEN")
    if not token:
        pytest.skip("ISIGN_API_TOKEN is not defined")
    return token


SANDBOX_USERS = [
    ("good1", "+37060000007", "51001091072", True),
    ("good2", "+37200000766", "11412090004", True),
    ("bad1", "+37060000001", "51001091006", False),  # operations will fail
    ("bad2", "+37060000420", "51001091013", False),  # completely made up
]
SANDBOX_USERS_GOOD = {
    "params": [(u[1], u[2]) for u in SANDBOX_USERS if u[3]],
    "ids": [f"{u[0]}" for u in SANDBOX_USERS if u[3]],
}
SANDBOX_USERS_BAD = {
    "params": [(u[1], u[2]) for u in SANDBOX_USERS if not u[3]],
    "ids": [f"{u[0]}" for u in SANDBOX_USERS if not u[3]],
}


@pytest.fixture(**SANDBOX_USERS_GOOD)
def sandbox_user_good(request: SubRequest) -> Tuple[str, str]:
    phone, code = request.param
    return phone, code


@pytest.fixture(**SANDBOX_USERS_BAD)
def sandbox_user_bad(request: SubRequest) -> Tuple[str, str]:
    phone, code = request.param
    return phone, code


@pytest.fixture()
def restore_config(request: SubRequest) -> None:
    import isign.functions
    originals = {
        "env": isign.functions.ISIGN_ENVIRONMENT,
        "tkn": isign.functions.ISIGN_ACCESS_TOKEN,
        "uag": isign.functions.ISIGN_USER_AGENT,
    }

    def restore() -> None:
        isign.functions.ISIGN_ENVIRONMENT = originals["env"]  # type: ignore
        isign.functions.ISIGN_ACCESS_TOKEN = originals["tkn"]  # type: ignore
        isign.functions.ISIGN_USER_AGENT = originals["uag"]  # type: ignore

    request.addfinalizer(restore)


@pytest.fixture()
def files() -> isign.Files:
    name = "test.pdf"
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), name))
    with open(path, "rb") as f:
        bin_content = f.read()

    sha1 = hashlib.sha1()
    sha1.update(bin_content)
    digest = sha1.hexdigest()

    content = base64.b64encode(bin_content).decode()

    return isign.files((name, digest, content))
