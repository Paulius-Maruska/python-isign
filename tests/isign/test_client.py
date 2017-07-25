import pytest
import requests_mock

from isign.client import ISignClient
from isign.connection import ISignConnection
from isign.environment import ISignEnvironment
from isign.error import ISignError
from isign.model import (
    file,
    files,
    MobileCertificateResponse,
    MobileLoginResponse,
    MobileLoginStatusResponse,
    MobileSignResponse,
    MobileSignStatusResponse,
    pdf,
)


def test_client_constructor() -> None:
    env = ISignEnvironment("foo", "foo.isign.io", "http")
    conn = ISignConnection("acctkn", "constructor_test", env)
    client = ISignClient(conn)
    assert client.connection == conn


def test_client_mobile_certificate() -> None:
    env = ISignEnvironment("foo", "foo.isign.io")
    conn = ISignConnection("acctkn", "test_client_mobile_certificate", env)
    client = ISignClient(conn)
    with requests_mock.mock() as rm:
        rm.post("https://foo.isign.io/mobile/certificate.json?access_token=acctkn",
                request_headers={"User-Agent": "test_client_mobile_certificate"},
                json={"status": "ok", "signing_certificate": {}, "authentication_certificate": {}},
                status_code=200)
        response = client.mobile_certificate("+37060000007", "51001091072")
    assert isinstance(response, MobileCertificateResponse)
    assert response.raw == {"status": "ok", "signing_certificate": {}, "authentication_certificate": {}}
    assert response.status == "ok"


def test_client_mobile_certificate_raises_when_status_not_good() -> None:
    env = ISignEnvironment("foo", "foo.isign.io")
    conn = ISignConnection("acctkn", "test_client_mobile_certificate_raises_when_status_not_good", env)
    client = ISignClient(conn)
    with requests_mock.mock() as rm:
        rm.post("https://foo.isign.io/mobile/certificate.json?access_token=acctkn",
                request_headers={"User-Agent": "test_client_mobile_certificate_raises_when_status_not_good"},
                json={"status": "error"},
                status_code=400)
        pytest.raises(ISignError, client.mobile_certificate, "+37060000007", "51001091072")


def test_client_mobile_login() -> None:
    env = ISignEnvironment("foo", "foo.isign.io")
    conn = ISignConnection("acctkn", "test_client_mobile_login", env)
    client = ISignClient(conn)
    with requests_mock.mock() as rm:
        rm.post("https://foo.isign.io/mobile/login.json?access_token=acctkn",
                request_headers={"User-Agent": "test_client_mobile_login"},
                json={"status": "ok", "certificate": {}, "token": "0123456789", "control_code": "1337"},
                status_code=200)
        response = client.mobile_login("+37060000007", "51001091072", language="EN", message="Login!")
    assert isinstance(response, MobileLoginResponse)
    assert response.raw == {"status": "ok", "certificate": {}, "token": "0123456789", "control_code": "1337"}
    assert response.status == "ok"


def test_client_mobile_login_raises_when_status_not_good() -> None:
    env = ISignEnvironment("foo", "foo.isign.io")
    conn = ISignConnection("acctkn", "test_client_mobile_login_raises_when_status_not_good", env)
    client = ISignClient(conn)
    with requests_mock.mock() as rm:
        rm.post("https://foo.isign.io/mobile/login.json?access_token=acctkn",
                request_headers={"User-Agent": "test_client_mobile_login_raises_when_status_not_good"},
                json={"status": "error"},
                status_code=400)
        pytest.raises(ISignError, client.mobile_login, "+37060000007", "51001091072")


def test_client_mobile_login_status() -> None:
    env = ISignEnvironment("foo", "foo.isign.io")
    conn = ISignConnection("acctkn", "test_client_mobile_login_status", env)
    client = ISignClient(conn)
    with requests_mock.mock() as rm:
        rm.get("https://foo.isign.io/mobile/login/status/1234567890.json?access_token=acctkn",
               request_headers={"User-Agent": "test_client_mobile_login_status"},
               json={"status": "waiting"},
               status_code=200)
        response = client.mobile_login_status("1234567890")
    assert isinstance(response, MobileLoginStatusResponse)
    assert response.raw == {"status": "waiting"}
    assert response.status == "waiting"


def test_client_mobile_login_status_raises_when_status_not_good() -> None:
    env = ISignEnvironment("foo", "foo.isign.io")
    conn = ISignConnection("acctkn", "test_client_mobile_login_status_raises_when_status_not_good", env)
    client = ISignClient(conn)
    with requests_mock.mock() as rm:
        rm.get("https://foo.isign.io/mobile/login/status/1234567890.json?access_token=acctkn",
               request_headers={"User-Agent": "test_client_mobile_login_status_raises_when_status_not_good"},
               json={"status": "error"},
               status_code=400)
        pytest.raises(ISignError, client.mobile_login_status, "1234567890")


def test_client_mobile_sign_raises_when_type_is_unrecognized() -> None:
    env = ISignEnvironment("foo", "foo.isign.io")
    conn = ISignConnection("acctkn", "test_client_mobile_sign", env)
    client = ISignClient(conn)
    assert pytest.raises(ValueError, client.mobile_sign, "+37060000007", "51001091072", "EN", "Login!", type="dummy")


def test_client_mobile_sign_raises_when_pdf_not_set_and_type_is_pdf() -> None:
    env = ISignEnvironment("foo", "foo.isign.io")
    conn = ISignConnection("acctkn", "test_client_mobile_sign", env)
    client = ISignClient(conn)
    assert pytest.raises(ValueError, client.mobile_sign, "+37060000007", "51001091072", "EN", "Login!", type="pdf")


def test_client_mobile_sign() -> None:
    env = ISignEnvironment("foo", "foo.isign.io")
    conn = ISignConnection("acctkn", "test_client_mobile_sign", env)
    client = ISignClient(conn)
    with requests_mock.mock() as rm:
        rm.post("https://foo.isign.io/mobile/sign.json?access_token=acctkn",
                request_headers={"User-Agent": "test_client_mobile_sign"},
                json={"status": "ok", "token": "0123456789", "control_code": "1337"},
                status_code=200)
        p = pdf(contact="Foo Bar",
                location="Vilnius",
                files=files(file("foo.pdf", "foo-digest", "foo-content")))
        response = client.mobile_sign("+37060000007", "51001091072", "EN", "Login!", pdf=p)
    assert isinstance(response, MobileSignResponse)
    assert response.raw == {"status": "ok", "token": "0123456789", "control_code": "1337"}
    assert response.status == "ok"


def test_client_mobile_sign_status() -> None:
    env = ISignEnvironment("foo", "foo.isign.io")
    conn = ISignConnection("acctkn", "test_client_mobile_login_status", env)
    client = ISignClient(conn)
    with requests_mock.mock() as rm:
        rm.get("https://foo.isign.io/mobile/sign/status/1234567890.json?access_token=acctkn",
               request_headers={"User-Agent": "test_client_mobile_login_status"},
               json={"status": "waiting"},
               status_code=200)
        response = client.mobile_sign_status("1234567890")
    assert isinstance(response, MobileSignStatusResponse)
    assert response.raw == {"status": "waiting"}
    assert response.status == "waiting"
