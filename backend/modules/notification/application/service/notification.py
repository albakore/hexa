from dataclasses import dataclass
from typing import Dict
from dependency_injector.providers import Singleton

from modules.notification.application.exception import ProviderSenderNotFoundException
from modules.notification.application.service.email_template import EmailTemplateService
from modules.notification.domain.command import CreateNotificationCommand, SendNotificationCommand
from modules.notification.domain.repository.notification import NotificationRepository
from modules.notification.domain.repository.sender_provider import SenderProviderPort
from modules.notification.domain.usecase.notification import NotificationUseCaseFactory


@dataclass
class NotificationService:
	
	notification_repository : NotificationRepository
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
	
	async def create_notification(self, command : CreateNotificationCommand):
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
	