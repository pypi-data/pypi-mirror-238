from typing import Optional

from pydantic import Field, UrlConstraints, ValidationError, ValidationInfo, field_validator
from pydantic_core import Url
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing_extensions import Annotated

SQLliteUrl = Annotated[Url, UrlConstraints(allowed_schemes=["file", "sqlite"])]


class SQLiteSettings(BaseSettings):
    model_config = SettingsConfigDict(case_sensitive=False)

    sqlite_path: Annotated[Optional[str], Field(description="Path to your sqlite database file", validate_default=True)] = None
    database_uri: Annotated[Optional[SQLliteUrl], Field(description="DB DSN", validate_default=True)] = None

    @field_validator("database_uri")
    @classmethod
    def assemble_db_connection(cls, v: Optional[str], info: ValidationInfo) -> SQLliteUrl:
        if v:
            return SQLliteUrl(v)

        if not info.data.get("sqlite_path"):
            raise ValidationError("Either database_uri or path must be set")

        return SQLliteUrl(f"sqlite://{info.data.get('sqlite_path')}")
