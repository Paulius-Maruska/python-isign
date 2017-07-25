import pytest
import requests_mock

import isign.functions
from isign import (
    file,
    files,
    ISignEnvironment,
    MobileCertificateResponse,
    MobileLoginResponse,
    MobileLoginStatusResponse,
    MobileSignResponse,
    MobileSignStatusResponse,
    pdf,
)


def test_use_config_sets_global_config(restore_config: None) -> None:
    env = ISignEnvironment("foo", "foo.isign.io")
    isign.functions.use_config("acctkn0", "foo-bar-0", env)
    assert isign.functions.ISIGN_ENVIRONMENT == env
    assert isign.functions.ISIGN_ACCESS_TOKEN == "acctkn0"
    assert isign.functions.ISIGN_USER_AGENT == "foo-bar-0"


def test_use_config_does_not_change_user_agent_and_environment_when_they_are_not_supplied(restore_config: None) -> None:
    env = isign.functions.ISIGN_ENVIRONMENT
    uag = isign.functions.ISIGN_USER_AGENT
    isign.functions.use_config("acctkn1")
    assert isign.functions.ISIGN_ENVIRONMENT == env
    assert isign.functions.ISIGN_ACCESS_TOKEN == "acctkn1"
    assert isign.functions.ISIGN_USER_AGENT == uag


def test_global_client_returns_client_configured_according_to_the_global_config(restore_config: None) -> None:
    env = ISignEnvironment("foo", "foo.isign.io")
    isign.functions.use_config("acctkn", "foo-bar-1", env)
    client = isign.functions.global_client()
    assert client.connection.access_token == "acctkn"
    assert client.connection.user_agent == "foo-bar-1"
    assert client.connection.environment == env


def test_global_client_raises_when_global_config_is_incorrect(restore_config: None) -> None:
    isign.functions.ISIGN_ACCESS_TOKEN = None
    isign.functions.ISIGN_USER_AGENT = None  # type: ignore
    isign.functions.ISIGN_ENVIRONMENT = None  # type: ignore
    assert pytest.raises(ValueError, isign.functions.global_client)
    isign.functions.ISIGN_ACCESS_TOKEN = "foo"
    assert pytest.raises(ValueError, isign.functions.global_client)
    isign.functions.ISIGN_USER_AGENT = "bar"
    assert pytest.raises(ValueError, isign.functions.global_client)


def test_mobile_certificate() -> None:
    env = ISignEnvironment("foo", "foo.isign.io")
    isign.functions.use_config("acctkn", "test_mobile_certificate", env)
    with requests_mock.mock() as rm:
        rm.post("https://foo.isign.io/mobile/certificate.json?access_token=acctkn",
                request_headers={"User-Agent": "test_mobile_certificate"},
                json={"status": "ok", "signing_certificate": {}, "authentication_certificate": {}},
                status_code=200)
        response = isign.functions.mobile_certificate("+37060000007", "51001091072")
    assert isinstance(response, MobileCertificateResponse)
    assert response.raw == {"status": "ok", "signing_certificate": {}, "authentication_certificate": {}}
    assert response.status == "ok"


def test_mobile_login() -> None:
    env = ISignEnvironment("foo", "foo.isign.io")
    isign.functions.use_config("acctkn", "test_mobile_login", env)
    with requests_mock.mock() as rm:
        rm.post("https://foo.isign.io/mobile/login.json?access_token=acctkn",
                request_headers={"User-Agent": "test_mobile_login"},
                json={"status": "ok", "certificate": {}, "token": "0123456789", "control_code": "1337"},
                status_code=200)
        response = isign.functions.mobile_login("+37060000007", "51001091072", language="EN", message="Login!")
    assert isinstance(response, MobileLoginResponse)
    assert response.raw == {"status": "ok", "certificate": {}, "token": "0123456789", "control_code": "1337"}
    assert response.status == "ok"


def test_mobile_login_status() -> None:
    env = ISignEnvironment("foo", "foo.isign.io")
    isign.functions.use_config("acctkn", "test_mobile_login_status", env)
    with requests_mock.mock() as rm:
        rm.get("https://foo.isign.io/mobile/login/status/1234567890.json?access_token=acctkn",
               request_headers={"User-Agent": "test_mobile_login_status"},
               json={"status": "waiting"},
               status_code=200)
        response = isign.functions.mobile_login_status("1234567890")
    assert isinstance(response, MobileLoginStatusResponse)
    assert response.raw == {"status": "waiting"}
    assert response.status == "waiting"


def test_mobile_sign() -> None:
    env = ISignEnvironment("foo", "foo.isign.io")
    isign.functions.use_config("acctkn", "test_mobile_sign", env)
    with requests_mock.mock() as rm:
        rm.post("https://foo.isign.io/mobile/sign.json?access_token=acctkn",
                request_headers={"User-Agent": "test_mobile_sign"},
                json={"status": "ok", "token": "0123456789", "control_code": "1337"},
                status_code=200)
        p = pdf(contact="Foo Bar",
                location="Vilnius",
                files=files(file("foo.pdf", "foo-digest", "foo-content")))
        response = isign.mobile_sign("+37060000007", "51001091072", "EN", "Login!", pdf=p)
    assert isinstance(response, MobileSignResponse)
    assert response.raw == {"status": "ok", "token": "0123456789", "control_code": "1337"}
    assert response.status == "ok"


def test_mobile_sign_status() -> None:
    env = ISignEnvironment("foo", "foo.isign.io")
    isign.functions.use_config("acctkn", "test_mobile_sign_status", env)
    with requests_mock.mock() as rm:
        rm.get("https://foo.isign.io/mobile/sign/status/1234567890.json?access_token=acctkn",
               request_headers={"User-Agent": "test_mobile_sign_status"},
               json={"status": "waiting"},
               status_code=200)
        response = isign.mobile_sign_status("1234567890")
    assert isinstance(response, MobileSignStatusResponse)
    assert response.raw == {"status": "waiting"}
    assert response.status == "waiting"
