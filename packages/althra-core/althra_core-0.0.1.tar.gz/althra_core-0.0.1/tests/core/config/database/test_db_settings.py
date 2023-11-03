import pydantic
import pytest
from althra.core.config.connections import DBSettings, PostgresSettings, SQLiteSettings
from pydantic_settings import BaseSettings


def test_db_settings_with_postgres() -> None:
    class T(BaseSettings):
        a: DBSettings

    t = T(
        a={
            "postgres_host": "postgres-server",
            "postgres_user": "postgres-user",
            "postgres_password": "postgres-password",
            "postgres_db": "postgres-db",
        }
    )
    assert isinstance(t.a, PostgresSettings)


def test_db_settings_sqlite() -> None:
    class T(BaseSettings):
        a: DBSettings

    t = T(
        a={
            "sqlite_path": "./file.db",
        }
    )
    assert isinstance(t.a, SQLiteSettings), t.a


def test_db_settings_sqlite_and_postgres():
    class T(BaseSettings):
        a: DBSettings

    with pytest.raises(pydantic.ValidationError):
        T(
            a={
                "sqlite_path": "./file.db",
                "postgres_host": "postgres-server",
                "postgres_user": "postgres-user",
                "postgres_password": "postgres-password",
                "postgres_db": "postgres-db",
            }
        )
