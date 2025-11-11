from fastapi import Body
from pydantic import BaseModel, Field

from modules.notification.domain.command import (
	CreateNotificationCommand,
	SendNotificationCommand,
)


class CreateNotificationRequest(CreateNotificationCommand): ...


class SendNotificationRequest(SendNotificationCommand): ...


class CreateEmailTemplateRequest(BaseModel):
	name: str = Field(...)
	description: str = Field(...)
	module: str = Field(...)
	template: str = Body(..., media_type="plain/text")
