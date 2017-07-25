from typing import Tuple

from isign.client import ISignClient
from isign.connection import ISignConnection
from isign.error import ISignError
from isign.model import Files, pdf


def test_isign_client_mobile_certificate_standard_flow(sandbox_token: str,
                                                       sandbox_user_good: Tuple[str, str]) -> None:
    phone, code = sandbox_user_good
    client = ISignClient(ISignConnection(sandbox_token, "python-isign", "sandbox"))
    response = client.mobile_certificate(phone, code)
    assert response.status == "ok"
    assert response.signing_certificate.subject.serial_number == code
    assert response.authentication_certificate.subject.serial_number == code


def test_isign_client_mobile_login_standard_flow(sandbox_token: str,
                                                 sandbox_user_good: Tuple[str, str]) -> None:
    phone, code = sandbox_user_good
    client = ISignClient(ISignConnection(sandbox_token, "python-isign", "sandbox"))
    login = client.mobile_login(phone, code, language="EN", message="Login to python-isign")
    assert login.status == "ok"
    assert login.control_code is not None

    # wait for status to change
    login_status = client.mobile_login_status(login.token)
    while login_status.status == "waiting":
        login_status = client.mobile_login_status(login.token)
    assert login_status.status == "ok"


def test_isign_client_mobile_sign_standard_flow(sandbox_token: str,
                                                sandbox_user_good: Tuple[str, str],
                                                files: Files) -> None:
    phone, code = sandbox_user_good
    client = ISignClient(ISignConnection(sandbox_token, "python-isign", "sandbox"))
    sign = client.mobile_sign(phone, code, "EN", "Sign this file",
                              type="pdf", pdf=pdf("Foo Bar", "Vilnius", files=files))
    assert sign.status == "ok"
    assert sign.control_code is not None

    # wait for status to change
    sign_status = client.mobile_sign_status(sign.token)
    while sign_status.status == "waiting":
        sign_status = client.mobile_sign_status(sign.token)
    assert sign_status.status == "ok"
    assert sign_status.signature_id is not None
    assert sign_status.file.raw is not None


def test_isign_client_mobile_certificate_standard_flow_with_bad_users(sandbox_token: str,
                                                                      sandbox_user_bad: Tuple[str, str]) -> None:
    phone, code = sandbox_user_bad
    client = ISignClient(ISignConnection(sandbox_token, "python-isign", "sandbox"))
    try:
        client.mobile_certificate(phone, code)
    except ISignError as err:
        assert err.error.status == "error"
        assert err.error.message is not None


def test_isign_client_mobile_login_standard_flow_with_bad_users(sandbox_token: str,
                                                                sandbox_user_bad: Tuple[str, str]) -> None:
    phone, code = sandbox_user_bad
    client = ISignClient(ISignConnection(sandbox_token, "python-isign", "sandbox"))
    try:
        client.mobile_login(phone, code, language="EN", message="Login to python-isign")
    except ISignError as err:
        assert err.error.status == "error"
        assert err.error.message is not None


def test_isign_client_mobile_sign_standard_flow_with_bad_users(sandbox_token: str,
                                                               sandbox_user_bad: Tuple[str, str],
                                                               files: Files) -> None:
    phone, code = sandbox_user_bad
    client = ISignClient(ISignConnection(sandbox_token, "python-isign", "sandbox"))
    try:
        client.mobile_sign(phone, code, "EN", "Sign this file",
                           type="pdf", pdf=pdf("Foo Bar", "Vilnius", files=files))
    except ISignError as err:
        assert err.error.status == "error"
        assert err.error.message is not None
