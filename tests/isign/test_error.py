from isign.error import ISignError


def test_error_constructor() -> None:
    err = ISignError("GET", "/foo/bar", 400, {"status": "error", "message": "This is bad", "error_code": 9000})
    assert err.method == "GET"
    assert err.path == "/foo/bar"
    assert err.status_code == 400
    assert err.error.raw == {"status": "error", "message": "This is bad", "error_code": 9000}


def test_error_str() -> None:
    err = ISignError("GET", "/foo/bar", 400, {"status": "error", "message": "This is bad", "error_code": 9000})
    assert str(err) == "ISignError: GET /foo/bar -> 400: This is bad (9000)"
