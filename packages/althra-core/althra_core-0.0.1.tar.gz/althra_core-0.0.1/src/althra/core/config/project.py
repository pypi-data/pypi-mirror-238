from typing import Mapping, Tuple

from althra.core.config.connections import DBSettings
from pydantic import Field
from pydantic_settings import BaseSettings, PydanticBaseSettingsSource, SettingsConfigDict


class ProjectSettings(BaseSettings):
    model_config = SettingsConfigDict(case_sensitive=False, env_nested_delimiter="__")
    project_name: str = Field(description="Project name")
    database: Mapping[str, DBSettings] = Field(description="Database settings")

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> Tuple[PydanticBaseSettingsSource, ...]:
        return file_secret_settings, env_settings, dotenv_settings, init_settings
