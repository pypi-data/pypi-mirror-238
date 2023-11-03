from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings


class AppSettings(BaseSettings):
    NAME: str = Field(description="App's name")
    FOLDER: Path = Field(description="App's folder")
    CONFIG_FILE_NAME: Path = Field(description="App's config file name", default=Path("app.yaml"))

    @property
    def config_file(self) -> Path:
        return self.FOLDER / self.CONFIG_FILE_NAME
