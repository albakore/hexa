from dataclasses import dataclass
from typing import Sequence
from core.db.transactional import Transactional

from modules.notification.domain.entity.email_template import EmailTemplate
from modules.notification.domain.exception import EmailTemplateNotFoundException
from modules.notification.domain.repository.email_template import (
	EmailTemplateRepository,
)
from modules.notification.domain.repository.sender_provider import SenderProviderPort


class UseCase: ...


@dataclass
class GetAllEmailTemplates(UseCase):
	email_template_repository: EmailTemplateRepository

	async def __call__(self) -> list[EmailTemplate] | Sequence[EmailTemplate]:
		email_templates = await self.email_template_repository.get_all_email_templates()
		return email_templates


@dataclass
class GetEmailTemplateById(UseCase):
	email_template_repository: EmailTemplateRepository

	async def __call__(self, id: int) -> EmailTemplate | None:
		email_template = await self.email_template_repository.get_email_template_by_id(
			id
		)
		return email_template


@dataclass
class GetEmailTemplateByName(UseCase):
	email_template_repository: EmailTemplateRepository

	async def __call__(self, name: str) -> EmailTemplate | None:
		email_template = (
			await self.email_template_repository.get_email_template_by_name(name)
		)
		return email_template


@dataclass
class GetEmailTemplateByModule(UseCase):
	email_template_repository: EmailTemplateRepository

	async def __call__(self, module: str) -> EmailTemplate | None:
		email_template = (
			await self.email_template_repository.get_email_template_by_module(module)
		)
		return email_template


@dataclass
class SaveEmailTemplate(UseCase):
	email_template_repository: EmailTemplateRepository

	@Transactional()
	async def __call__(self, template: EmailTemplate) -> EmailTemplate:
		new_email_template = await self.email_template_repository.save_email_template(
			template
		)
		return new_email_template


@dataclass
class DeleteEmailTemplate(UseCase):
	email_template_repository: EmailTemplateRepository

	@Transactional()
	async def __call__(self, id: int) -> None:
		email_template = await self.email_template_repository.get_email_template_by_id(
			id
		)
		if not email_template:
			raise EmailTemplateNotFoundException
		await self.email_template_repository.delete_email_template(email_template)


@dataclass
class SendEmailTemplate(UseCase):
	email_template_sender: SenderProviderPort

	async def __call__(
		self, receiver_email: list[str], subject: str, body: str
	) -> None:
		await self.email_template_sender.send(None, receiver_email, subject, body)


@dataclass
class EmailTemplateUseCaseFactory:
	email_template_repository: EmailTemplateRepository
	email_template_sender: SenderProviderPort

	def __post_init__(self):
		self.get_all_email_templates = GetAllEmailTemplates(
			self.email_template_repository
		)
		self.get_email_template_by_id = GetEmailTemplateById(
			self.email_template_repository
		)
		self.get_email_template_by_name = GetEmailTemplateByName(
			self.email_template_repository
		)
		self.get_email_template_by_module = GetEmailTemplateByModule(
			self.email_template_repository
		)
		self.save_email_template = SaveEmailTemplate(self.email_template_repository)
		self.delete_email_template = DeleteEmailTemplate(self.email_template_repository)
		self.send_email_template = SendEmailTemplate(self.email_template_sender)
