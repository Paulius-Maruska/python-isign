from isign.model.base import Base


def test_base_constructor() -> None:
    r = Base({"foo": "bar", "dummy": 1337})
    assert r.raw == {"foo": "bar", "dummy": 1337}


def test_base_constructor_no_argument() -> None:
    r = Base()
    assert r.raw == {}
