from isign.model.error import FieldError


def test_field_error_constructor() -> None:
    ef = FieldError({
        "message": "Field is wrong",
        "error_code": 123,
        "field": "[test][0][name]",
    })
    assert ef.raw == {
        "message": "Field is wrong",
        "error_code": 123,
        "field": "[test][0][name]",
    }


def test_field_error_correctly_extracts_information_from_raw_dict() -> None:
    fei = FieldError({
        "message": "Field is wrong",
        "error_code": 123,
        "field": "[test][0][name]",
    })
    assert fei.error_code == 123
    assert fei.message == "Field is wrong"
    assert fei.field == "[test][0][name]"


def test_field_error_str() -> None:
    fei = FieldError({
        "message": "Field is wrong",
        "error_code": 123,
        "field": "[test][0][name]",
    })
    assert str(fei) == "[test][0][name] - Field is wrong (123)"
