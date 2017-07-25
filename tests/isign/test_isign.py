from typing import Tuple

import isign


def test_isign_get_mobile_certificate_of_a_user(restore_config: None,
                                                sandbox_token: str,
                                                sandbox_user_good: Tuple[str, str]) -> None:
    phone, code = sandbox_user_good
    isign.use_config(access_token=sandbox_token,
                     user_agent="python-isign",
                     environment="sandbox")
    response = isign.mobile_certificate(phone, code)
    assert response.status == "ok"
    assert response.signing_certificate.subject.serial_number == code
    assert response.authentication_certificate.subject.serial_number == code


def test_isign_login_operation(restore_config: None,
                               sandbox_token: str,
                               sandbox_user_good: Tuple[str, str]) -> None:
    phone, code = sandbox_user_good
    isign.use_config(access_token=sandbox_token,
                     user_agent="python-isign",
                     environment="sandbox")
    login = isign.mobile_login(phone, code, language="EN", message="Login to python-isign")
    assert login.status == "ok"
    assert login.control_code is not None

    # wait for status to change
    login_status = isign.mobile_login_status(login.token)
    while login_status.status == "waiting":
        login_status = isign.mobile_login_status(login.token)
    assert login_status.status == "ok"


def test_isign_sign_operation(restore_config: None,
                              sandbox_token: str,
                              sandbox_user_good: Tuple[str, str],
                              files: isign.Files) -> None:
    phone, code = sandbox_user_good
    isign.use_config(access_token=sandbox_token,
                     user_agent="python-isign",
                     environment="sandbox")
    sign = isign.mobile_sign(phone, code,
                             language="EN",
                             message="Login to python-isign",
                             type="pdf",
                             pdf=isign.pdf("Foo Bar", "Vilnius", files=files))
    assert sign.status == "ok"
    assert sign.control_code is not None

    # wait for status to change
    sign_status = isign.mobile_sign_status(sign.token)
    while sign_status.status == "waiting":
        sign_status = isign.mobile_sign_status(sign.token)
    assert sign_status.status == "ok"
    assert sign_status.signature_id is not None
    assert sign_status.file.raw is not None
