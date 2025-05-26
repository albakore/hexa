from enum import Enum
from pydantic_settings import BaseSettings
import os
import typer

class Environment(Enum):
	LOCAL = "local"
	DEVELOPMENT = "development"
	PRODUCTION = "production"

class Settings(BaseSettings):
	ENV : str = "local"
	DATABASE_URL : str = "sqlite+aiosqlite///db.sqlite"

class LocalSettings(Settings):
	ENV : str = "local"

class DevelopmentSettings(Settings):
	ENV : str = "development"

class ProductionSettings(Settings):
	ENV : str = "production"


def get_config(env_type: str | None) -> Settings:
	env_list = {
		Environment.LOCAL: LocalSettings(),
		Environment.DEVELOPMENT: DevelopmentSettings(),
		Environment.PRODUCTION: ProductionSettings(),
	}
	if not env_type:
		return env_list[Environment.LOCAL]

	return env_list[Environment(env_type)]

env = get_config(os.environ.get("ENV"))