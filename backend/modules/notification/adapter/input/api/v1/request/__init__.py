from fastapi import Body
from pydantic import BaseModel, Field

from modules.notification.domain.command import CreateNotificationCommand


class CreateNotificationRequest(CreateNotificationCommand): ...


class CreateEmailTemplateRequest(BaseModel):
    name: str = Field(...)
    description: str = Field(...)
    module: str = Field(...)
    template: str  = Body(..., media_type="plain/text")
    