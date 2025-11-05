from enum import Enum
from pydantic_settings import BaseSettings, SettingsConfigDict
import os
import typer


class Environment(Enum):
	LOCAL = "local"
	DEVELOPMENT = "development"
	PRODUCTION = "production"


class Settings(BaseSettings):
	ENV: str = "local"
	BACKEND_PATH: str = ""
	DATABASE_URL: str = "postgresql+asyncpg://hexa:hexa@localhost:5432/hexa"
	REDIS_URL: str = (
		"redis://localhost:6379/0?password=eYVX7EwVmmxKPCDmwMtyKVge8oLd2t81"
	)
	REDIS_PASSWORD: str = "eYVX7EwVmmxKPCDmwMtyKVge8oLd2t81"
	# DATABASE_URL : str = "sqlite+aiosqlite:///db.sqlite"
	JWT_SECRET_KEY: str = "omelettedufromage"
	JWT_ALGORITHM: str = "HS256"
	JWT_ACCESS_TOKEN_EXPIRATION_MINUTES: int = 15
	JWT_REFRESH_TOKEN_EXPIRATION_DAYS: int = 7

	EMAIL_SMTP_SERVER: str
	EMAIL_SMTP_PORT: str
	EMAIL_SMTP_APPLICATION: str
	EMAIL_SMTP_MAILSENDER: str
	EMAIL_SMTP_USERNAME: str
	EMAIL_SMTP_PASSWORD: str

	AWS_ACCESS_KEY: str
	AWS_ACCESS_SECRET_KEY: str
	AWS_ACCESS_REGION: str
	AWS_ACCESS_BUCKET_NAME: str

	WEBHOOK_SLACK_NOTIFY_MLA : str
	WEBHOOK_SLACK_API_TOKEN_MLA : str

	RABBITMQ_URL: str = "amqp://hexa:hexa@localhost:5672/"

	OPENAPI_EXPORT_DIR: str = "docs/openapi.json"

	YIQI_BASE_URL: str = "ooolee"
	YIQI_API_TOKEN: str = "uooleeee"
	YIQI_LAST_INVOICE_UPDATE: list = [2025, 4, 7]
	YIQI_SCHEMA: int = 000

	model_config = SettingsConfigDict(
		env_file=".env", env_file_encoding="utf-8", extra="ignore"
	)


class LocalSettings(Settings):
	ENV: str = "local"


class DevelopmentSettings(Settings):
	ENV: str = "development"


class ProductionSettings(Settings):
	ENV: str = "production"


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
