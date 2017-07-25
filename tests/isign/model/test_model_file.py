import pytest

from isign.model.file import File, file, Files, files


def test_file_constructor() -> None:
    f = File({"name": "file.pdf", "digest": "asdfgh", "content": "foo-bar-baz"})
    assert f.raw == {"name": "file.pdf", "digest": "asdfgh", "content": "foo-bar-baz"}


def test_file_correctly_extracts_information_from_raw_dict() -> None:
    f = File({"name": "file.pdf", "digest": "asdfgh", "content": "foo-bar-baz"})
    assert f.name == "file.pdf"
    assert f.digest == "asdfgh"
    assert f.content == "foo-bar-baz"


def test_files_constructor() -> None:
    f = Files([{"name": "file.pdf", "digest": "asdfgh", "content": "foo-bar-baz"}])
    assert f.raw == [{"name": "file.pdf", "digest": "asdfgh", "content": "foo-bar-baz"}]


def test_files_item_access_accesses_raw_list() -> None:
    f = Files([{"name": "file1.pdf", "digest": "asdfgh", "content": "foo-bar-baz"},
               {"name": "file2.pdf", "digest": "zxcvbn", "content": "faa-bor-boz"}])
    assert f[0].raw == f.raw[0]
    assert f[1].raw == f.raw[1]


def test_files_item_assignment_assigns_to_raw_list() -> None:
    f = Files([{"name": "file1.pdf", "digest": "asdfgh", "content": "foo-bar-baz"},
               {"name": "file2.pdf", "digest": "zxcvbn", "content": "faa-bor-boz"}])
    f[1] = File({"name": "file2upd.pdf", "digest": "zxcvbnm", "content": "faa-bor-boz-moroz"})
    assert f[1].raw == {"name": "file2upd.pdf", "digest": "zxcvbnm", "content": "faa-bor-boz-moroz"}


def test_files_item_deletion_deletes_from_raw_list() -> None:
    f = Files([{"name": "file1.pdf", "digest": "asdfgh", "content": "foo-bar-baz"},
               {"name": "file2.pdf", "digest": "zxcvbn", "content": "faa-bor-boz"}])
    del f[0]
    assert len(f) == 1


def test_files_append_adds_new_file_to_the_end() -> None:
    f = Files([{"name": "file1.pdf", "digest": "asdfgh", "content": "foo-bar-baz"},
               {"name": "file2.pdf", "digest": "zxcvbn", "content": "faa-bor-boz"}])
    f.append(File({"name": "file2upd.pdf", "digest": "zxcvbnm", "content": "faa-bor-boz-moroz"}))
    assert len(f) == 3
    assert f[2].raw == {"name": "file2upd.pdf", "digest": "zxcvbnm", "content": "faa-bor-boz-moroz"}


def test_file_function_creates_file_object() -> None:
    f = file("foo.pdf", "bar", "dummy")
    assert isinstance(f, File)
    assert f.name == "foo.pdf"
    assert f.digest == "bar"
    assert f.content == "dummy"


def test_files_function_can_be_called_without_arguments() -> None:
    f = files()
    assert isinstance(f, Files)
    assert len(f) == 0


def test_files_function_raises_when_argument_is_bad() -> None:
    assert pytest.raises(ValueError, files, file("foo.pdf", "foo", "foo-content"), 1337)


def test_files_function_accepts_file_objects_as_arguments() -> None:
    f = files(file("foo.pdf", "foo", "foo-content"),
              file("bar.pdf", "bar", "bar-content"))
    assert isinstance(f, Files)
    assert len(f) == 2
    assert f[0].name == "foo.pdf"
    assert f[1].name == "bar.pdf"


def test_files_function_accepts_tuples_as_arguments() -> None:
    f = files(("foo.pdf", "foo", "foo-content"),
              ("bar.pdf", "bar", "bar-content"))
    assert isinstance(f, Files)
    assert len(f) == 2
    assert f[0].name == "foo.pdf"
    assert f[1].name == "bar.pdf"


def test_files_function_accepts_mixture_of_file_objects_and_tuples_as_arguments() -> None:
    f = files(file("foo.pdf", "foo", "foo-content"),
              ("bar.pdf", "bar", "bar-content"))
    assert isinstance(f, Files)
    assert len(f) == 2
    assert f[0].name == "foo.pdf"
    assert f[1].name == "bar.pdf"
