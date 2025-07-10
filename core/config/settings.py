from enum import Enum
from pydantic_settings import BaseSettings,SettingsConfigDict
import os
import typer

class Environment(Enum):
	LOCAL = "local"
	DEVELOPMENT = "development"
	PRODUCTION = "production"

class Settings(BaseSettings):
	ENV : str = "local"
	BACKEND_PATH : str = ""
	DATABASE_URL : str = "postgresql+asyncpg://hexa:hexa@localhost:5432/hexa" 
	REDIS_URL : str = "redis://localhost:6379/0?password=eYVX7EwVmmxKPCDmwMtyKVge8oLd2t81" 
	# DATABASE_URL : str = "sqlite+aiosqlite:///db.sqlite"
	JWT_SECRET_KEY : str = "omelettedufromage"
	JWT_ALGORITHM : str = "HS256"
	JWT_ACCESS_TOKEN_EXPIRATION_MINUTES : int = 15
	JWT_REFRESH_TOKEN_EXPIRATION_DAYS : int = 7

	OPENAPI_EXPORT_DIR : str = "docs/openapi.json"

	model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')

class LocalSettings(Settings):
	ENV : str = "local"

class DevelopmentSettings(Settings):
	ENV : str = "development"

class ProductionSettings(Settings):
	ENV : str = "production"


def get_config(env_type: str | None) -> Settings:
	env_list = {
		Environment.LOCAL: LocalSettings,
		Environment.DEVELOPMENT: DevelopmentSettings,
		Environment.PRODUCTION: ProductionSettings,
	}
	if not env_type:
		return env_list[Environment.LOCAL]()

	return env_list[Environment(env_type)]()

env = get_config(os.environ.get("ENV"))