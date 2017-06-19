import pytest
import requests_mock

from isign.client import ISignClient
from isign.connection import ISignConnection
from isign.environment import ISignEnvironment
from isign.error import ISignError
from isign.model import MobileCertificateResponse


def test_client_constructor() -> None:
    env = ISignEnvironment("foo", "foo.isign.io", "http")
    conn = ISignConnection("acctkn", "constructor_test", env)
    client = ISignClient(conn)
    assert client.connection == conn


def test_client_mobile_certificate() -> None:
    env = ISignEnvironment("foo", "foo.isign.io")
    conn = ISignConnection("acctkn", "constructor_test", env)
    client = ISignClient(conn)
    with requests_mock.mock() as rm:
        rm.post("https://foo.isign.io/mobile/certificate.json?access_token=acctkn",
                request_headers={"User-Agent": "constructor_test"},
                json={"status": "ok", "signing_certificate": {}, "authentication_certificate": {}},
                status_code=200)
        response = client.mobile_certificate("+37060000007", "51001091072")
    assert isinstance(response, MobileCertificateResponse)
    assert response.raw == {"status": "ok", "signing_certificate": {}, "authentication_certificate": {}}
    assert response.status == "ok"


def test_client_mobile_certificate_raises_when_status_not_good() -> None:
    env = ISignEnvironment("foo", "foo.isign.io")
    conn = ISignConnection("acctkn", "constructor_test", env)
    client = ISignClient(conn)
    with requests_mock.mock() as rm:
        rm.post("https://foo.isign.io/mobile/certificate.json?access_token=acctkn",
                request_headers={"User-Agent": "constructor_test"},
                json={"status": "error"},
                status_code=400)
        pytest.raises(ISignError, client.mobile_certificate, "+37060000007", "51001091072")
