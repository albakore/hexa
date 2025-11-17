from abc import ABC, abstractmethod
from typing import Sequence
from modules.notification.domain.entity import Notification


class NotificationRepository(ABC):
	@abstractmethod
	async def get_all_notifications(
		self,
	) -> list[Notification] | Sequence[Notification]: ...

	@abstractmethod
	async def get_notification_by_id(self, id: int) -> Notification | None: ...

	@abstractmethod
	async def get_notifications_by_user(
		self, id_user: int
	) -> list[Notification] | Sequence[Notification]: ...

	@abstractmethod
	async def create_notification(self, notification: Notification) -> Notification: ...

	@abstractmethod
	async def delete_notification(
		self, notification: Notification
	) -> Notification | None: ...
