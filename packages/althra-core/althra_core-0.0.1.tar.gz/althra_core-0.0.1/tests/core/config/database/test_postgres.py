import pytest
from althra.core.config.connections.postgres import PostgresSettings


def test_with_connection_details_is_successfull() -> None:
    postgres_connection = PostgresSettings(
        postgres_host="postgres-server",
        postgres_user="postgres-user",
        postgres_password="postgres-password",  # noqa: S106
        postgres_db="postgres-db",
    )
    assert (
        str(postgres_connection.database_uri) == "postgresql://postgres-user:postgres-password@postgres-server/postgres-db"
    ), postgres_connection.database_uri


@pytest.mark.parametrize(
    "field_name",
    [
        "postgres_user",
        "postgres_password",
        "postgres_db",
    ],
)
def test_with_partial_connection_details_fails(field_name: str) -> None:
    values = {
        "postgres_host": "postgres-server",
        "postgres_user": "postgres-user",
        "postgres_password": "postgres-password",
        "postgres_db": "postgres-db",
    }
    values.pop(field_name)
    with pytest.warns(UserWarning):
        PostgresSettings(**values)


def test_with_uri_and_no_details_is_successfull() -> None:
    PostgresSettings(
        database_uri="postgresql://postgres-user:postgres-password@postgres-server/postgres-db",
    )


@pytest.mark.parametrize(
    "field_name, field_value",
    [
        ("postgres_host", "postgres-server"),
        ("postgres_user", "postgres-user"),
        ("postgres_password", "<PASSWORD>"),
        ("postgres_db", "postgres-db"),
    ],
)
def test_with_connection_with_uri_forbids_other_fields(field_name, field_value) -> None:
    with pytest.raises(ValueError):
        PostgresSettings(
            **{field_name: field_value},
            database_uri="postgresql://postgres-user:postgres-password@postgres-server/postgres-db",
        )
