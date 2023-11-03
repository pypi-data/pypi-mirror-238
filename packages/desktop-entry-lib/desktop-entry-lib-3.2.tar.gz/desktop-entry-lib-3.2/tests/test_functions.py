import desktop_entry_lib
import pyfakefs
import pytest
import os


def test_version() -> None:
    assert isinstance(desktop_entry_lib.__version__, str)


def test_get_xdg_data_dirs(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("XDG_DATA_DIRS", "/hello/world:/test/123:/foo/bar")
    assert desktop_entry_lib.get_xdg_data_dirs() == ["/hello/world", "/test/123", "/foo/bar"]

    monkeypatch.setenv("XDG_DATA_DIRS", "/hello/world:/test/123:/foo/bar:")
    assert desktop_entry_lib.get_xdg_data_dirs() == ["/hello/world", "/test/123", "/foo/bar"]

    monkeypatch.delenv("XDG_DATA_DIRS")
    assert desktop_entry_lib.get_xdg_data_dirs() == [os.path.expanduser("~/.local/share"), "/usr/share"]


def test_get_icon_path(monkeypatch: pytest.MonkeyPatch, fs: pyfakefs.fake_filesystem.FakeFilesystem) -> None:
    fs.os = pyfakefs.fake_filesystem.OSType.LINUX

    monkeypatch.delenv("XDG_DATA_DIRS", False)

    assert desktop_entry_lib.get_icon_path("test") is None

    fs.create_file("/usr/share/pixmaps/test.png")
    assert desktop_entry_lib.get_icon_path("test") == "/usr/share/pixmaps/test.png"

    fs.create_file("/usr/share/icons/hicolor/invalid/apps/test.png")
    assert desktop_entry_lib.get_icon_path("test") == "/usr/share/pixmaps/test.png"

    fs.create_file("/usr/share/icons/hicolor/128x128/apps/test.png")
    assert desktop_entry_lib.get_icon_path("test") == "/usr/share/icons/hicolor/128x128/apps/test.png"

    fs.create_file("/usr/share/icons/hicolor/scalable/apps/test.png")
    assert desktop_entry_lib.get_icon_path("test") == "/usr/share/icons/hicolor/128x128/apps/test.png"

    fs.create_file("/usr/share/icons/hicolor/scalable/apps/test.svg")
    assert desktop_entry_lib.get_icon_path("test") == "/usr/share/icons/hicolor/scalable/apps/test.svg"


def test_is_action_identifier_valid() -> None:
    assert desktop_entry_lib.is_action_identifier_valid("hello") is True
    assert desktop_entry_lib.is_action_identifier_valid("hello-world") is True
    assert desktop_entry_lib.is_action_identifier_valid("hello_world") is False


def test_is_custom_key_name_valid() -> None:
    assert desktop_entry_lib.is_custom_key_name_valid("Hello") is False
    assert desktop_entry_lib.is_custom_key_name_valid("X-Hello") is True
    assert desktop_entry_lib.is_custom_key_name_valid("X-Hello-World") is True
    assert desktop_entry_lib.is_custom_key_name_valid("X-Hello_World") is False
    assert desktop_entry_lib.is_custom_key_name_valid("X-Hello-World[Lang]") is True
    assert desktop_entry_lib.is_custom_key_name_valid("X-Hello-World[Lang") is False
    assert desktop_entry_lib.is_custom_key_name_valid("X-Hello-World[]") is False
