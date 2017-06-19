from isign.model.certificate import Certificate
from isign.model.mobile_certificate_response import MobileCertificateResponse


def test_error_correctly_extracts_information_from_raw_dict() -> None:
    mcr = MobileCertificateResponse({
        "status": "ok",
        "signing_certificate": {
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
        "authentication_certificate": {
            "name": "/C=LT/O=DummyCorp/OU=Authenticating/CN=FOO,BAR,31234567890/SN=FOO/GN=BAR/serialNumber=31234567890",
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
            "value": "YmF6LWJhci1mb28=",
        },
        "country": "LT",
        "code": "31234567890",
        "name": "BAR",
        "surname": "FOO",
    })
    assert mcr.status == "ok"
    assert isinstance(mcr.signing_certificate, Certificate)
    assert mcr.signing_certificate.value.as_str() == "foo-bar-baz"
    assert isinstance(mcr.authentication_certificate, Certificate)
    assert mcr.authentication_certificate.value.as_str() == "baz-bar-foo"
    assert mcr.country == "LT"
    assert mcr.code == "31234567890"
    assert mcr.name == "BAR"
    assert mcr.surname == "FOO"
