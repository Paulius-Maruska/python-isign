import pytest

from isign.environment import (
    get_default_environment,
    ISignEnvironment,
    LIVE,
    SANDBOX
)


def test_environment_constructor() -> None:
    env = ISignEnvironment("foo", "foo.isign.io", "http")
    assert env.name == "foo"
    assert env.netloc == "foo.isign.io"
    assert env.scheme == "http"

    env = ISignEnvironment("bar", "bar.isign.io")
    assert env.name == "bar"
    assert env.netloc == "bar.isign.io"
    assert env.scheme == "https"


def test_environment_repr() -> None:
    env = ISignEnvironment("foo", "foo.isign.io", "http")
    assert repr(env) == "ISignEnvironment(name='foo', netloc='foo.isign.io', scheme='http')"

    env = ISignEnvironment("bar", "bar.isign.io")
    assert repr(env) == "ISignEnvironment(name='bar', netloc='bar.isign.io', scheme='https')"


def test_environment_str() -> None:
    env = ISignEnvironment("foo", "foo.isign.io", "http")
    assert str(env) == "< isign env 'foo' foo.isign.io >"

    env = ISignEnvironment("bar", "bar.isign.io")
    assert str(env) == "< isign env 'bar' bar.isign.io >"


def test_environment_construct_url_raises_value_error_when_access_token_is_missing() -> None:
    env = ISignEnvironment("foo", "foo.isign.io")
    assert pytest.raises(ValueError, env.construct_url, "", "/something")
    assert pytest.raises(ValueError, env.construct_url, None, "/something")


def test_environment_construct_url() -> None:
    env = ISignEnvironment("foo", "foo.isign.io")
    assert env.construct_url("r4nd0mt0k3n", "/some/path") == "https://foo.isign.io/some/path?access_token=r4nd0mt0k3n"


def test_sandbox() -> None:
    assert isinstance(SANDBOX, ISignEnvironment)
    assert SANDBOX.name == "sandbox"
    assert SANDBOX.netloc == "developers.isign.io"
    assert SANDBOX.scheme == "https"


def test_live() -> None:
    assert isinstance(LIVE, ISignEnvironment)
    assert LIVE.name == "live"
    assert LIVE.netloc == "api2.isign.io"
    assert LIVE.scheme == "https"


def test_get_default_environment_raises_when_name_unknown() -> None:
    assert pytest.raises(ValueError, get_default_environment, "dummy")


@pytest.mark.parametrize("name", ["sandbox", "live"])
def test_get_default_environment_returns_correct_environment_object(name: str) -> None:
    env = get_default_environment(name)
    assert isinstance(env, ISignEnvironment)
    assert env.name == name
