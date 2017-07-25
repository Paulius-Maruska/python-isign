from isign.model.base import BaseDict, BaseList


def test_base_dict_constructor() -> None:
    r = BaseDict({"foo": "bar", "dummy": 1337})
    assert r.raw == {"foo": "bar", "dummy": 1337}


def test_base_dict_constructor_no_argument_sets_empty_dict() -> None:
    r = BaseDict()
    assert r.raw == {}


def test_base_dict_len_returns_length_of_raw_field() -> None:
    r = BaseDict({"foo": "bar", "dummy": 1337})
    assert len(r) == 2


def test_base_list_constructor() -> None:
    r = BaseList([1, 2, 3])
    assert r.raw == [1, 2, 3]


def test_base_list_constructor_no_argument_sets_empty_dict() -> None:
    r = BaseList()
    assert r.raw == []


def test_base_len_returns_length_of_raw_field() -> None:
    r = BaseList([1, 2, 3])
    assert len(r) == 3
