from isign.model.certificate import Certificate
from isign.model.mobile_login_response import MobileLoginResponse, MobileLoginStatusResponse


def test_mobile_login_response_correctly_extracts_information_from_raw_dict() -> None:
    mlr = MobileLoginResponse({
        "status": "ok",
        "certificate": {
            "name": "/C=LT/O=DummyCorp/OU=Signing/CN=FOO,BAR,31234567890/SN=FOO/GN=BAR/serialNumber=31234567890",
            "subject": {
                "country": "LT",
                "organisation": "DummyCorp",
                "organisation_unit": "Signing",
                "common_name": "FOO,BAR,31234567890",
                "surname": "FOO",
                "name": "BAR",
                "serial_number": "31234567890",
            },
            "issuer": {
                "country": "LT",
                "organisation": "CertAuthority",
                "common_name": "admin@ca.lt of CertAuthority",
                "email": "admin@ca.lt",
            },
            "valid_from": "2017-01-20T04:20:13+03:00",
            "valid_to": "2017-12-31T23:59:59+03:00",
            "value": "Zm9vLWJhci1iYXo=",
        },
        "country": "LT",
        "code": "31234567890",
        "name": "BAR",
        "surname": "FOO",
        "token": "1234567890",
        "control_code": "1234",
    })
    assert mlr.status == "ok"
    assert isinstance(mlr.certificate, Certificate)
    assert mlr.certificate.value.as_str() == "foo-bar-baz"
    assert mlr.country == "LT"
    assert mlr.code == "31234567890"
    assert mlr.name == "BAR"
    assert mlr.surname == "FOO"
    assert mlr.token == "1234567890"
    assert mlr.control_code == "1234"


def test_mobile_login_status_response_correctly_extracts_information_from_raw_dict() -> None:
    mlsr = MobileLoginStatusResponse({"status": "waiting"})
    assert mlsr.status == "waiting"
