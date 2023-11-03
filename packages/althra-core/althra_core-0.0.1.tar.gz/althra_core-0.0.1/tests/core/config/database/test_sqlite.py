import pytest
from althra.core.config.connections.sqlite import SQLiteSettings


@pytest.mark.parametrize("path", ["db.sqlite", "../db.sqlite"])
def test_with_file_is_successful(path: str) -> None:
    file_connection = SQLiteSettings(sqlite_path=path)
    assert str(file_connection.database_uri) == f"sqlite://{path}"


@pytest.mark.parametrize("path", ["db.sqlite", "../db.sqlite"])
def test_with_db_uri_is_successful(path: str) -> None:
    file_connection = SQLiteSettings(database_uri=f"sqlite://{path}")
    assert str(file_connection.database_uri) == f"sqlite://{path}"


@pytest.mark.xfail
def test_with_in_memory_is_successful() -> None:
    memory_connection = SQLiteSettings(
        sqlite_path=":memory:",
    )
    assert str(memory_connection.database_uri) == "sqlite://:memory:"
