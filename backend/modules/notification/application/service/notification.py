from dataclasses import dataclass
from typing import Any, Dict

from dependency_injector.providers import Singleton

from modules.notification.application.exception import ProviderSenderNotFoundException
from modules.notification.application.service.email_template import EmailTemplateService
from modules.notification.application.usecase.notification import (
	NotificationUseCaseFactory,
)
from modules.notification.domain.command import (
	CreateNotificationCommand,
	SendEmailNotificationCommand,
	SendNotificationCommand,
)
from modules.notification.domain.exception import EmailTemplateNotFoundException
from modules.notification.domain.repository.notification import NotificationRepository
from modules.notification.domain.repository.sender_provider import SenderProviderPort


@dataclass
class NotificationService:
	notification_repository: NotificationRepository
	sender_providers: Dict[str, Singleton[SenderProviderPort]]
	email_template_service: EmailTemplateService

	def __post_init__(self):
		self.usecase = NotificationUseCaseFactory(self.notification_repository)

	async def get_all_notifications(self):
		notifications = await self.usecase.get_all_notifications()
		return notifications

	async def get_notification_by_id(self, id: int):
		notification = await self.usecase.get_notification_by_id(id)
		return notification

	async def create_notification(self, command: CreateNotificationCommand):
		new_notification = await self.usecase.create_notification(command)
		return new_notification

	async def delete_notification(self, id: int):
		await self.usecase.delete_notification(id)

	async def send_notification(self, command: SendNotificationCommand | dict):
		if isinstance(command, dict):
			command = SendNotificationCommand.model_validate(command)
		sender = self.sender_providers.get(command.sender)
		if not sender:
			raise ProviderSenderNotFoundException

		await sender().send(command.notification)

	async def send_email_notification(
		self, command: SendEmailNotificationCommand | dict[str, Any]
	):
		if isinstance(command, dict):
			command = SendEmailNotificationCommand.model_validate(command)
		template = await self.email_template_service.get_email_template_by_name(
			command.template_name
		)

		if not template:
			raise EmailTemplateNotFoundException

		# Renderizar template con el payload (TypedDict es compatible con dict)
		template_rendered = await self.email_template_service.render_email_template(
			template,
			command.data_injection,  # type: ignore[arg-type]
		)

		# Crear el diccionario de notificación con el body renderizado
		notification_data: Dict[str, Any] = {
			"to": command.notification.to,
			"subject": command.notification.subject,
			"body": template_rendered,
		}

		data: Dict[str, Any] = {
			"sender": "email",
			"notification": notification_data,
		}
		await self.send_notification(data)

	def _prepare_template(self, template: bytes, data: dict) -> str:
		template_decoded = template.decode()
		for key, value in data.items():
			template_decoded = template_decoded.replace(key, value)
		return template_decoded
