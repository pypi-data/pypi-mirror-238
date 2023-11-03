import pytest
from althra.core.config.connections import PostgresSettings, SQLiteSettings
from althra.core.config.project import ProjectSettings


def test_project_with_valid_dict_is_sucessfull() -> None:
    project = ProjectSettings(project_name="test", database={"sqlite": {"sqlite_path": "./file.db"}})
    assert "sqlite" in project.database
    assert isinstance(project.database["sqlite"], SQLiteSettings)


def test_project_with_env_is_sucessfull(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("project_name", "foo")
    monkeypatch.setenv("database__sqlite__sqlite_path", "foo.db")
    project = ProjectSettings()
    assert "sqlite" in project.database
    assert isinstance(project.database["sqlite"], SQLiteSettings)
    assert str(project.database["sqlite"].database_uri) == "sqlite://foo.db"


def test_project_with_env_and_object_takes_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("project_name", "foo")
    monkeypatch.setenv("database__sqlite__sqlite_path", "foo.db")
    project = ProjectSettings(database={"sqlite": {"sqlite_path": "bar.db"}})

    assert isinstance(project.database["sqlite"], SQLiteSettings)
    assert str(project.database["sqlite"].database_uri) == "sqlite://foo.db"


def test_project_with_invalid_dict_fails() -> None:
    with pytest.raises(ValueError):
        ProjectSettings(project_name="test", database={"hello": {"sqlite_path": "./file.db", "host": "localhost"}})


def test_project_with_clashing_env_and_dict_fails(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("database__hello__host", "localhost")
    with pytest.raises(ValueError):
        ProjectSettings(project_name="test", database={"hello": {"sqlite_path": "./file.db", "host": "localhost"}})


def test_project_with_several_connections_is_successful(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("database__hello__postgres_host", "localhost")

    project = ProjectSettings(project_name="test", database={"world": {"sqlite_path": "./file.db"}})

    assert "hello" in project.database
    assert isinstance(project.database["hello"], PostgresSettings)

    assert "world" in project.database
    assert isinstance(project.database["world"], SQLiteSettings)
