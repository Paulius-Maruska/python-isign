from isign.model.response import Response


def test_response_constructor() -> None:
    r = Response({"status": "ok", "data": "foo"})
    assert r.raw == {"status": "ok", "data": "foo"}


def test_response_correctly_extracts_status_from_raw_dict() -> None:
    assert Response({"status": "ok"}).status == "ok"
    assert Response({"status": "error"}).status == "error"
