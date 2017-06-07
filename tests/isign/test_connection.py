import pytest
import requests_mock

from isign.connection import ISignConnection
from isign.environment import ISignEnvironment
from isign.error import ISignError


def test_connection_constructor_with_environment_object() -> None:
    env = ISignEnvironment("foo", "foo.isign.io", "http")
    conn = ISignConnection("acctkn", "constructor_test", env)
    assert conn.access_token == "acctkn"
    assert conn.user_agent == "constructor_test"
    assert conn.environment == env


def test_connection_constructor_with_default_environment_name() -> None:
    conn = ISignConnection("acctoken", "constructor_test", "sandbox")
    assert conn.access_token == "acctoken"
    assert isinstance(conn.environment, ISignEnvironment)
    assert conn.environment.name == "sandbox"


def test_connection_constructor_raises_when_environment_value_is_wrong() -> None:
    assert pytest.raises(ValueError, ISignConnection, "at", "ua", 11)


def test_connection_repr() -> None:
    env = ISignEnvironment("foo", "foo.isign.io", "http")
    conn = ISignConnection("acctkn", "repr_test", env)
    assert repr(conn) == f"ISignConnection(access_token='acctkn', user_agent='repr_test', environment={env!r})"


def test_connection_str() -> None:
    env = ISignEnvironment("foo", "foo.isign.io", "http")
    conn = ISignConnection("acctkn", environment=env)
    assert str(conn) == f"< isign conn for {env} >"


def test_connection_get_calls_requests_get_and_returns_parsed_json() -> None:
    env = ISignEnvironment("foo", "foo.isign.io", "http")
    conn = ISignConnection("acctkn", "usragnt", env)

    with requests_mock.mock() as rm:
        rm.get("http://foo.isign.io/bar?access_token=acctkn",
               request_headers={"User-Agent": "usragnt"},
               json={"test status": "passing"},
               status_code=200)
        content = conn.get("/bar")
    assert content == {"test status": "passing"}


def test_connection_get_calls_requests_get_and_raises_when_status_code_is_400() -> None:
    env = ISignEnvironment("foo", "foo.isign.io", "http")
    conn = ISignConnection("acctkn", "usragnt", env)

    with requests_mock.mock() as rm:
        rm.get("http://foo.isign.io/bar?access_token=acctkn",
               request_headers={"User-Agent": "usragnt"},
               json={"test status": "error"},
               status_code=400)
        assert pytest.raises(ISignError, conn.get, "/bar")


def test_connection_post_calls_requests_get_and_returns_parsed_json() -> None:
    env = ISignEnvironment("foo", "foo.isign.io", "http")
    conn = ISignConnection("acctkn", "usrbgnt", env)

    with requests_mock.mock() as rm:
        rm.post("http://foo.isign.io/baz?access_token=acctkn",
                request_headers={"User-Agent": "usrbgnt",
                                 "Content-Type": "application/json"},
                json={"test status": "passing"},
                status_code=200)
        content = conn.post("/baz", {"input": "data"})
    assert content == {"test status": "passing"}


def test_connection_post_calls_requests_get_and_raises_when_status_code_is_400() -> None:
    env = ISignEnvironment("foo", "foo.isign.io", "http")
    conn = ISignConnection("acctkn", "usrbgnt", env)

    with requests_mock.mock() as rm:
        rm.post("http://foo.isign.io/baz?access_token=acctkn",
                request_headers={"User-Agent": "usrbgnt",
                                 "Content-Type": "application/json"},
                json={"test status": "passing"},
                status_code=400)
        assert pytest.raises(ISignError, conn.post, "/baz", {"input": "data"})
