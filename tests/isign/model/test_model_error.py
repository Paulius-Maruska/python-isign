from isign.model.error import Error


def test_error_correctly_extracts_information_from_raw_dict() -> None:
    err = Error({
        "status": "error",
        "error_code": 1337,
        "message": "Request is wrong",
        "errors": [{
            "message": "Field is wrong",
            "error_code": 123,
            "field": "[test][0][name]",
        }],
    })
    assert err.status == "error"
    assert err.error_code == 1337
    assert err.message == "Request is wrong"
    assert len(err.errors) == 1
    assert err.errors[0].error_code == 123
    assert err.errors[0].message == "Field is wrong"
    assert err.errors[0].field == "[test][0][name]"
    del err.raw["errors"]
    assert len(err.errors) == 0


def test_error_str() -> None:
    err = Error({
        "status": "error",
        "error_code": 1337,
        "message": "Request is wrong",
        "errors": [{
            "message": "Field is wrong",
            "error_code": 123,
            "field": "[test][0][name]",
        }],
    })
    assert str(err) == "Request is wrong (1337):\n  [test][0][name] - Field is wrong (123)"
    del err.raw["errors"]
    assert str(err) == "Request is wrong (1337)"
