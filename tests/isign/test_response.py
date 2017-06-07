from isign.response import Response


def test_response_constructor() -> None:
    content = {"status": "ok", "foo": "bar"}
    response = Response(content)
    assert response.content == content


def test_response_correctly_extracts_information_from_content_dict() -> None:
    response = Response({"status": "ok", "foo": "bar"})
    assert response.status == "ok"
