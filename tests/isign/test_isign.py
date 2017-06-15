from typing import Tuple

from isign.client import ISignClient
from isign.connection import ISignConnection
from isign.error import ISignError


def test_isign_client_mobile_certificate_standard_flow(sandbox_token: str,
                                                       sandbox_user_good: Tuple[str, str]) -> None:
    phone, code = sandbox_user_good
    client = ISignClient(ISignConnection(sandbox_token, "python-isign", "sandbox"))
    response = client.mobile_certificate(phone, code)
    assert response.status == "ok"

    assert "signing_certificate" in response.raw
    assert "subject" in response.raw["signing_certificate"]
    assert "serial_number" in response.raw["signing_certificate"]["subject"]
    assert response.raw["signing_certificate"]["subject"]["serial_number"] == code

    assert "authentication_certificate" in response.raw
    assert "subject" in response.raw["authentication_certificate"]
    assert "serial_number" in response.raw["authentication_certificate"]["subject"]
    assert response.raw["authentication_certificate"]["subject"]["serial_number"] == code


def test_isign_client_mobile_certificate_standard_flow_with_bad_users(sandbox_token: str,
                                                                      sandbox_user_bad: Tuple[str, str]) -> None:
    phone, code = sandbox_user_bad
    client = ISignClient(ISignConnection(sandbox_token, "python-isign", "sandbox"))
    try:
        client.mobile_certificate(phone, code)
    except ISignError as err:
        assert err.error.status == "error"
        assert err.error.message is not None
