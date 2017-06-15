from isign.model.error import ErrorField


def test_field_error_info_correctly_extracts_information_from_raw_dict() -> None:
    fei = ErrorField({
        "message": "Field is wrong",
        "error_code": 123,
        "field": "[test][0][name]",
    })
    assert fei.error_code == 123
    assert fei.message == "Field is wrong"
    assert fei.field == "[test][0][name]"


def test_field_error_info_str() -> None:
    fei = ErrorField({
        "message": "Field is wrong",
        "error_code": 123,
        "field": "[test][0][name]",
    })
    assert str(fei) == "[test][0][name] - Field is wrong (123)"
