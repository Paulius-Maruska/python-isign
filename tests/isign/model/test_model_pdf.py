import pytest

from isign.model.file import file, files
from isign.model.pdf import PDF, pdf


def test_pdf_constructor() -> None:
    r = PDF({"contact": "Bob", "location": "Vilnius", "files": []})
    assert r.raw == {"contact": "Bob", "location": "Vilnius", "files": []}


def test_pdf_allows_construction_without_parameter() -> None:
    r = PDF()
    assert r.raw == {}


def test_pdf_allows_assigning_values_later_on() -> None:
    r = PDF()
    r.contact = "Bob"
    r.location = "Kaunas"
    r.signing_purpose = "registration"
    r.reason = "Heck Yeah!"
    r.files.append(file("foo.pdf", "dgst", "dummy"))
    assert r.raw == {"contact": "Bob",
                     "location": "Kaunas",
                     "signing_purpose": "registration",
                     "reason": "Heck Yeah!",
                     "files": [{"name": "foo.pdf", "digest": "dgst", "content": "dummy"}]}


def test_pdf_allows_accessing_values_through_properties() -> None:
    r = PDF({"contact": "Bob",
             "location": "Kaunas",
             "signing_purpose": "registration",
             "reason": "Heck Yeah!",
             "files": [{"name": "foo.pdf", "digest": "dgst", "content": "dummy"}]})
    assert r.contact == "Bob"
    assert r.location == "Kaunas"
    assert r.signing_purpose == "registration"
    assert r.reason == "Heck Yeah!"
    assert r.files.raw == [{"name": "foo.pdf", "digest": "dgst", "content": "dummy"}]


def test_pdf_signing_purpose_raises_when_assigning_bad_value() -> None:
    r = PDF()

    def dummy(value: str) -> None:
        r.signing_purpose = value

    assert pytest.raises(ValueError, dummy, "bad value")


def test_pdf_accessing_files_property_automatically_adds_empty_files_list_into_raw() -> None:
    r = PDF()
    assert r.raw == {}
    assert len(r.files) == 0
    assert r.raw == {"files": []}


def test_pdf_accessing_files_property_returns_existing_files_list() -> None:
    r = PDF({"files": [{"name": "foo.pdf"}]})
    assert r.raw == {"files": [{"name": "foo.pdf"}]}
    assert len(r.files) == 1
    assert r.raw == {"files": [{"name": "foo.pdf"}]}


def test_pdf_function_creates_pdf_object() -> None:
    r = pdf("Bob", "Vilnius")
    assert isinstance(r, PDF)
    assert r.contact == "Bob"
    assert r.location == "Vilnius"
    # the defaults
    assert r.signing_purpose == "signature"
    assert r.reason == ""
    assert r.files.raw == []


def test_pdf_function_sets_optional_values_when_they_are_provided() -> None:
    r = pdf("Bob", "Vilnius", "registration", "Woohoo!")
    assert isinstance(r, PDF)
    assert r.contact == "Bob"
    assert r.location == "Vilnius"
    assert r.signing_purpose == "registration"
    assert r.reason == "Woohoo!"


def test_pdf_function_raises_when_files_list_contains_bad_value() -> None:
    assert pytest.raises(ValueError, pdf, "Bob", "Vilnius", files=1337)


def test_pdf_function_sets_files_when_files_object_provided() -> None:
    r = pdf("Bob", "Vilnius", files=files(file("foo.pdf", "foo", "foo-content"),
                                          file("bar.pdf", "bar", "bar-content")))
    assert isinstance(r, PDF)
    assert r.contact == "Bob"
    assert r.location == "Vilnius"
    assert r.files.raw == [{"name": "foo.pdf", "digest": "foo", "content": "foo-content"},
                           {"name": "bar.pdf", "digest": "bar", "content": "bar-content"}]


def test_pdf_function_sets_files_when_files_provided_as_list_of_file_objects() -> None:
    r = pdf("Bob", "Vilnius", files=[file("foo.pdf", "foo", "foo-content"),
                                     file("bar.pdf", "bar", "bar-content")])
    assert isinstance(r, PDF)
    assert r.contact == "Bob"
    assert r.location == "Vilnius"
    assert r.files.raw == [{"name": "foo.pdf", "digest": "foo", "content": "foo-content"},
                           {"name": "bar.pdf", "digest": "bar", "content": "bar-content"}]


def test_pdf_function_sets_files_when_files_provided_as_list_of_tuples() -> None:
    r = pdf("Bob", "Vilnius", files=[("foo.pdf", "foo", "foo-content"),
                                     ("bar.pdf", "bar", "bar-content")])
    assert isinstance(r, PDF)
    assert r.contact == "Bob"
    assert r.location == "Vilnius"
    assert r.files.raw == [{"name": "foo.pdf", "digest": "foo", "content": "foo-content"},
                           {"name": "bar.pdf", "digest": "bar", "content": "bar-content"}]
