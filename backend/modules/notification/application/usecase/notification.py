from dataclasses import dataclass
from typing import Sequence
from core.db.transactional import Transactional

from modules.notification.domain.command import CreateNotificationCommand
from modules.notification.domain.entity.notification import Notification
from modules.notification.domain.exception import NotificationNotFoundException
from modules.notification.domain.repository.notification import NotificationRepository


class UseCase: ...


@dataclass
class GetAllNotifications(UseCase):
	notification_repository: NotificationRepository

	async def __call__(self) -> list[Notification] | Sequence[Notification]:
		notifications = await self.notification_repository.get_all_notifications()
		return notifications


@dataclass
class GetNotificationById(UseCase):
	notification_repository: NotificationRepository

	async def __call__(self, id: int) -> Notification | None:
		notifications = await self.notification_repository.get_notification_by_id(id)
		return notifications


@dataclass
class CreateNotification(UseCase):
	notification_repository: NotificationRepository

	@Transactional()
	async def __call__(self, command: CreateNotificationCommand) -> Notification:
		notification = Notification.model_validate(command)
		new_notification = await self.notification_repository.create_notification(
			notification
		)
		return new_notification


@dataclass
class DeleteNotification(UseCase):
	notification_repository: NotificationRepository

	@Transactional()
	async def __call__(self, id: int) -> Notification | None:
		notification = await self.notification_repository.get_notification_by_id(id)
		if not notification:
			raise NotificationNotFoundException
		await self.notification_repository.delete_notification(notification)
		return notification


@dataclass
class NotificationUseCaseFactory:
	notification_repository: NotificationRepository

	def __post_init__(self):
		self.get_all_notifications = GetAllNotifications(self.notification_repository)
		self.get_notification_by_id = GetNotificationById(self.notification_repository)
		self.create_notification = CreateNotification(self.notification_repository)
		self.delete_notification = DeleteNotification(self.notification_repository)
