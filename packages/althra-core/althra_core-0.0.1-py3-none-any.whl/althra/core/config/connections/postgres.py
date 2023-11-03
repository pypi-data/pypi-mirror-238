import warnings
from typing import Dict, Literal, Optional

from pydantic import Field, PostgresDsn, ValidationInfo, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing_extensions import Annotated


class PostgresSettings(BaseSettings):
    """
    A Pydantic model for Postgres database settings.

    Attributes:
    -----------
    postgres_scheme: Literal[
        'postgres',
        'postgresql',
        'postgresql+asyncpg',
        'postgresql+pg8000',
        'postgresql+psycopg',
        'postgresql+psycopg2',
        'postgresql+psycopg2cffi',
        'postgresql+py-postgresql',
        'postgresql+pygresql',
    ] = Field(description="Scheme for your postgres", default="postgresql")
        The scheme for the postgres database.

    postgres_host: Annotated[Optional[str], Field(description="Host name or IP address for your postgres", validate_default=True)] = None
        The host name or IP address for the postgres database.

    postgres_user: Annotated[Optional[str], Field(description="Username for your postgres HOST", validate_default=True)] = None
        The username for the postgres database.

    postgres_password: Annotated[Optional[str], Field(description="Password for your postgres HOST", validate_default=True)] = None
        The password for the postgres database.

    postgres_db: Annotated[Optional[str], Field(description="Name of your postgres database", validate_default=True)] = None
        The name of the postgres database.

    database_uri: Annotated[Optional[PostgresDsn], Field(description="Postgres database URI string", validate_default=True)] = None
        The URI string for the postgres database.

    Methods:
    --------
    assemble_db_connection(cls, v: Optional[str], info: ValidationInfo) -> PostgresDsn:
        Assembles the database connection.

    check_no_values_when_database_uri(cls, data: Any) -> Any:
        Checks that no values are specified when using database_uri.
    """

    model_config = SettingsConfigDict(case_sensitive=False)

    postgres_scheme: Literal[
        "postgres",
        "postgresql",
        "postgresql+asyncpg",
        "postgresql+pg8000",
        "postgresql+psycopg",
        "postgresql+psycopg2",
        "postgresql+psycopg2cffi",
        "postgresql+py-postgresql",
        "postgresql+pygresql",
    ] = Field(description="Scheme for your postgres", default="postgresql")
    postgres_host: Annotated[Optional[str], Field(description="Host name or IP address for your postgres", validate_default=True)] = None
    postgres_user: Annotated[Optional[str], Field(description="Username for your postgres HOST", validate_default=True)] = None
    postgres_password: Annotated[Optional[str], Field(description="Password for your postgres HOST", validate_default=True)] = None
    postgres_db: Annotated[Optional[str], Field(description="Name of your postgres database", validate_default=True)] = None
    database_uri: Annotated[Optional[PostgresDsn], Field(description="DB DSN", validate_default=True)] = None

    @field_validator("database_uri")
    @classmethod
    def assemble_db_connection(cls, v: Optional[str], info: ValidationInfo) -> PostgresDsn:
        """
        Assembles the database connection.

        Parameters:
        -----------
        v: Optional[str]
            The URI string for the postgres database.
        info: ValidationInfo
            The validation information.

        Returns:
        --------
        PostgresDsn
            The assembled database connection.
        """
        if v is not None:
            return PostgresDsn(v)
        else:
            return PostgresDsn.build(
                scheme=str(info.data.get("postgres_scheme")),
                username=info.data.get("postgres_user"),
                password=info.data.get("postgres_password"),
                host=info.data.get("postgres_host"),
                path=info.data.get("postgres_db"),
            )

    @model_validator(mode="before")
    @classmethod
    def check_no_values_when_database_uri(cls, data: Dict[str, str]) -> Dict[str, str]:
        """
        Checks that no values are specified when using database_uri.

        Parameters:
        -----------
        data: Any
            The data to check.

        Returns:
        --------
        Any
            The checked data.
        """
        if "database_uri" in data:
            if len(data) > 1:
                raise ValueError("You cannot specify both database_uri and postgres_* fields")  #
            return data
        for field in ["postgres_host", "postgres_user", "postgres_password", "postgres_db"]:
            if not data.get(field):
                warnings.warn(f"Missing {field} in PostgresSettings", stacklevel=1, category=UserWarning)
        return data
