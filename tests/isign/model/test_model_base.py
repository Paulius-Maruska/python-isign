from isign.model.base import Base


def test_base_constructor() -> None:
    raw = {"status": "ok", "foo": "bar"}
    response = Base(raw)
    assert response.raw == raw
