from isign.model.mobile_sign_response import MobileSignResponse, MobileSignStatusResponse


def test_mobile_sign_response_correctly_extracts_information_from_raw_dict() -> None:
    msr = MobileSignResponse({
        "status": "ok",
        "token": "1234567890",
        "control_code": "1234",
    })
    assert msr.status == "ok"
    assert msr.token == "1234567890"
    assert msr.control_code == "1234"


def test_mobile_sign_status_response_extracts_information_from_raw_dict() -> None:
    mssr = MobileSignStatusResponse({
        "status": "ok",
        "signature_id": "sigid",
        "file": {
            "name": "foo.pdf",
            "digest": "foo-digest",
            "content": "foo-content",
        },
    })
    assert mssr.status == "ok"
    assert mssr.signature_id == "sigid"
    assert mssr.file.raw == {"name": "foo.pdf", "digest": "foo-digest", "content": "foo-content"}
