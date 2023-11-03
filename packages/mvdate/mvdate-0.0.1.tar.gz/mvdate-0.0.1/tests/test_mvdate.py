"""Tests for mvdate."""
from pathlib import Path

import pytest

from mvdate import mvdate


@pytest.mark.parametrize(("base", "ext", "n_matches"), [("./mvdate/", "py", 3), ("./tests/", "txt", 1)])
def test_find(base: str, ext: str, n_matches: int) -> None:
    """Test files are found correctly."""
    files_found = list(mvdate.find(base, ext))
    assert len(files_found) == n_matches


@pytest.mark.skip(reason="Need to figure out why mtime isn't the same on CI as locally")
@pytest.mark.parametrize(("test_file", "creation"), [("tests/resources/test.txt", 1697919000.0)])
def test_get_file_date(test_file: str, creation: float) -> None:
    """Test extraction of file date."""
    assert mvdate.get_file_date(Path(test_file)) == creation


def test_get_file_date_typeerror() -> None:
    """Check get_file_date() raises a TypeError if it doesn't get a reference to a file."""
    with pytest.raises(FileNotFoundError):
        assert mvdate.get_file_date("not_a_file")


@pytest.mark.parametrize(("target_dir"), [("./"), ("./test/nested"), ("../test"), ("../test/nested/parent")])
def test_create_target_dir(target_dir: str, tmp_path: Path) -> None:
    """Test target directory is created."""
    mvdate.create_target_dir(tmp_path / target_dir)
    assert Path(tmp_path / target_dir).is_dir()


@pytest.mark.parametrize(
    ("test_file", "nesting", "sep", "target_dir"),
    [
        ("tests/resources/test.txt", "Y", False, "2023"),
        ("tests/resources/test.txt", "m", False, "2023/11"),
        ("tests/resources/test.txt", "d", False, "2023/11/02"),
        ("tests/resources/test.txt", "H", False, "2023/11/02/21"),
        ("tests/resources/test.txt", "M", False, "2023/11/02/21/11"),
        ("tests/resources/test.txt", "M", True, "2023-11-02-21-11"),
        ("tests/resources/test.txt", None, False, "2023/11/02"),
        ("tests/resources/test.txt", None, True, "2023-11-02"),
    ],
)
def test_extract_date_time(test_file: str, nesting: str, sep: bool, target_dir: str) -> None:
    """Test extraction of date/time to string."""
    creation_date = mvdate.get_file_date(test_file)
    assert mvdate.extract_date_time(creation_date, nesting, sep) == target_dir


@pytest.mark.parametrize(
    ("test_file", "nesting", "sep", "target_dir"),
    [
        ("tests/resources/test.txt", "Y", False, "2023"),
        ("tests/resources/test.txt", "m", False, "2023/11"),
        ("tests/resources/test.txt", "d", False, "2023/11/02"),
        ("tests/resources/test.txt", "H", False, "2023/11/02/21"),
        ("tests/resources/test.txt", "M", False, "2023/11/02/21/11"),
        ("tests/resources/test.txt", "M", True, "2023-11-02-21-11"),
        ("tests/resources/test.txt", None, False, "2023/11/02"),
        ("tests/resources/test.txt", None, True, "2023-11-02"),
    ],
)
def test_create_file_parent(test_file: str, nesting: str, sep: bool, target_dir: str, tmp_path: Path) -> None:
    """Integration test to check extraction of creation date, deriving target directory and creation work together."""
    creation_date = mvdate.get_file_date(test_file)
    nested_dir = mvdate.extract_date_time(creation_date, nesting, sep)
    mvdate.create_target_dir(tmp_path / nested_dir)
    assert Path(tmp_path / target_dir).is_dir()


@pytest.mark.parametrize(
    ("source", "destination", "exception"),
    [
        (Path("test/resource/does_not_exist.txt"), "does_not_exist.txt", FileNotFoundError),
        (Path("test/resource/test.txt"), "somewhere/test.txt", FileNotFoundError),
    ],
)
def test_move_file_errors(source: Path, destination: Path, exception, tmp_path: Path) -> None:
    """Test FileNotFoundError raised when either source or target file/directory do not exist."""
    with pytest.raises(exception):
        assert mvdate.move_file(source, tmp_path / destination)


def test_move_file(tmp_path: Path) -> None:
    """Test move_file() function."""
    test_file = tmp_path / "test_file.txt"
    test_file.touch()
    destination = tmp_path / "nested"
    destination.mkdir()
    mvdate.move_file(test_file, destination)
    target_file = destination / test_file.name
    assert target_file.is_file()


# https://stackoverflow.com/a/76977976/1444043
# @pytest.mark.parametrize(
#     ("args"),
#     [
#         ([f"-b ./", "-e txt", "-d ./dest", "-n Y"]),
#     ],
# )
# def test_entry_point(args: list, tmp_path: Path) -> None:
#     """Integration test for the main() function."""
#     for x in range(0, 10):
#         tmp_file = Path(tmp_path / f"test{x}.txt")
#         tmp_file.touch()

#         assert tmp_file.is_file()
#     args = [re.sub(r"./", f"{tmp_path}/", x) for x in args]
#     print(f"[test] args")
#     print(list(tmp_path.rglob(f"**/*.txt")))
#     print(f"[test] tmp_path.is_dir() : {tmp_path.is_dir()}")
#     assert tmp_path.is_dir()
#     destination = Path(tmp_path / "dest")
#     destination.mkdir()
#     print(f"[test] tmp_path.is_dir() : {tmp_path.is_dir()}")
#     assert destination.is_dir()
#     mvdate.main(args=args)
#     moved_files = list(destination.rglob("**/*.txt"))
#     print(f"@@@@ moved_files : {moved_files}")
#     assert len(moved_files) == 10


# @pytest.mark.parametrize(
#     ("args"),
#     [
#         (["-v", "--version"]),
#     ],
# )
# def test_entry_point_reports_version(args: list, capsys) -> None:
#     """Check the version is reported"""
#     mvdate.main(args=args)
#     print(capsys)
#     assert re.search("Installed version of mvdate", capsys)
