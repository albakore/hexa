import uuid

from pydantic import BaseModel


class CreateNotificationCommand(BaseModel):
	user_id: uuid.UUID | None = None
	name: str = "user_registration"
	type: str = ""
	message: str = ""
	date_sent: str = ""
	active: bool = True


class EditEmailTemplateCommand(BaseModel):
	name: str | None = None
	description: str | None = None
	template_html: bytes | None = None
	module: str | None = None


class SendNotificationCommand(BaseModel):
	notification: dict
	sender: str


class EmailBasicInformationDTO(BaseModel):
	to: list[str]
	subject: str


class SendEmailNotificationCommand(BaseModel):
	template_name: str
	notification: EmailBasicInformationDTO
	data_injection: dict
