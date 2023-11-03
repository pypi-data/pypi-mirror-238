from typing import Union

from althra.core.config.connections.postgres import PostgresSettings
from althra.core.config.connections.sqlite import SQLiteSettings

DBSettings = Union[SQLiteSettings, PostgresSettings]
