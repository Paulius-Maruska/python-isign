from datetime import datetime, timedelta, timezone

from isign.model.certificate import (
    Certificate,
    CertificateIssuer,
    CertificateSubject,
)
from isign.model.parsed import (
    Base64Str,
    DateTimeStr,
)


def test_certificate_subject_constructor() -> None:
    cs = CertificateSubject({"foo": "bar"})
    assert cs.raw == {"foo": "bar"}


def test_certificate_subject_correctly_extracts_values_from_raw_dict() -> None:
    cs = CertificateSubject({
        "country": "LT",
        "organisation": "DummyCorp",
        "organisation_unit": "Signing",
        "common_name": "FOO,BAR,31234567890",
        "surname": "FOO",
        "name": "BAR",
        "serial_number": "31234567890",
    })
    assert cs.country == "LT"
    assert cs.organisation == "DummyCorp"
    assert cs.organisation_unit == "Signing"
    assert cs.common_name == "FOO,BAR,31234567890"
    assert cs.surname == "FOO"
    assert cs.name == "BAR"
    assert cs.serial_number == "31234567890"


def test_certificate_issuer_contructor() -> None:
    ci = CertificateIssuer({"foo": "bar"})
    assert ci.raw == {"foo": "bar"}


def test_certificate_issuer_correctly_extracts_values_from_raw_dict() -> None:
    ci = CertificateIssuer({
        "country": "LT",
        "organisation": "CertAuthority",
        "common_name": "admin@ca.lt of CertAuthority",
        "email": "admin@ca.lt",
    })
    assert ci.country == "LT"
    assert ci.organisation == "CertAuthority"
    assert ci.common_name == "admin@ca.lt of CertAuthority"
    assert ci.email == "admin@ca.lt"


def test_certificate_contructor() -> None:
    c = Certificate({"foo": "bar"})
    assert c.raw == {"foo": "bar"}


def test_certificate_correctly_extracts_values_from_raw_dict() -> None:
    c = Certificate({
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
    })
    assert c.name == "/C=LT/O=DummyCorp/OU=Signing/CN=FOO,BAR,31234567890/SN=FOO/GN=BAR/serialNumber=31234567890"
    assert isinstance(c.subject, CertificateSubject)
    assert c.subject.common_name == "FOO,BAR,31234567890"
    assert isinstance(c.issuer, CertificateIssuer)
    assert c.issuer.common_name == "admin@ca.lt of CertAuthority"
    assert isinstance(c.valid_from, DateTimeStr)
    assert c.valid_from.as_datetime() == datetime(2017, 1, 20, 4, 20, 13, 0, tzinfo=timezone(timedelta(hours=3)))
    assert isinstance(c.valid_to, DateTimeStr)
    assert c.valid_to.as_datetime() == datetime(2017, 12, 31, 23, 59, 59, 0, tzinfo=timezone(timedelta(hours=3)))
    assert isinstance(c.value, Base64Str)
    assert c.value.as_str() == "foo-bar-baz"
