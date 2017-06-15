from isign.model.base import Base


def test_base_constructor() -> None:
    raw = {"status": "ok", "foo": "bar"}
    response = Base(raw)
    assert response.raw == raw


def test_base_correctly_extracts_information_from_content_dict() -> None:
    assert Base({"status": "ok"}).status == "ok"
    assert Base({"status": "error"}).status == "error"
