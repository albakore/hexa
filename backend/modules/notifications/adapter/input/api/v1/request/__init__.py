from fastapi import Body, Query
from pydantic import BaseModel, Field
from modules.notifications.domain.command import CreateNotificationCommand

class CreateNotificationRequest(CreateNotificationCommand): ...

class CreateEmailTemplateRequest(BaseModel):
    name: str = Field(...)
    description: str = Field(...)
    module: str = Field(...)
    template: str  = Body(..., media_type="plain/text")