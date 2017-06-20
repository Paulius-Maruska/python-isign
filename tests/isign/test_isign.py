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
