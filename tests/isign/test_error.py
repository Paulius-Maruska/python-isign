from isign.error import ISignError, ISignFieldErrorInfo


def test_field_error_info_constructor() -> None:
    data = {
        "message": "Field is wrong",
        "error_code": 123,
        "field": "[test][0][name]",
    }
    fei = ISignFieldErrorInfo(data)
    assert fei.data == data


def test_field_error_info_correctly_extracts_information_from_error_dict() -> None:
    fei = ISignFieldErrorInfo({
        "message": "Field is wrong",
        "error_code": 123,
        "field": "[test][0][name]",
    })
    assert fei.error_code == 123
    assert fei.message == "Field is wrong"
    assert fei.field == "[test][0][name]"


def test_field_error_info_str() -> None:
    fei = ISignFieldErrorInfo({
        "message": "Field is wrong",
        "error_code": 123,
        "field": "[test][0][name]",
    })
    assert str(fei) == "123: [test][0][name]: Field is wrong"


def test_error_constructor() -> None:
    request = {
        "phone": "+37066655544",
    }
    response = {
        "status": "error",
        "error_code": 1337,
        "message": "Request is wrong",
    }
    err = ISignError("POST", "/foo/bar", 400, response, request)
    assert err.method == "POST"
    assert err.url == "/foo/bar"
    assert err.status_code == 400
    assert err.response == response
    assert err.request == request


def test_error_correctly_extracts_information_from_error_dict() -> None:
    err = ISignError("POST", "/foo/123", 400, {
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
    del err.response["errors"]
    assert len(err.errors) == 0


def test_error_str() -> None:
    err = ISignError("POST", "/foo", 400, {
        "status": "error",
        "error_code": 1337,
        "message": "Request is wrong",
        "errors": [{
            "message": "Field is wrong",
            "error_code": 123,
            "field": "[test][0][name]",
        }],
    }, {
        "phone": "+37066655544",
    })
    assert str(err) == "ISignError: POST /foo: 1337: Request is wrong: [\n  123: [test][0][name]: Field is wrong\n]"
    del err.response["errors"]
    assert str(err) == "ISignError: POST /foo: 1337: Request is wrong"
