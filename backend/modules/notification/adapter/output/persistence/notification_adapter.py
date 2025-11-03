from dataclasses import dataclass
from typing import Sequence

from modules.notification.domain.entity import Notification
from modules.notification.domain.repository.notification import NotificationRepository


@dataclass
class NotificationRepositoryAdapter(NotificationRepository):
    notification_repository: NotificationRepository

    async def get_all_notifications(self) -> list[Notification] | Sequence[Notification]:
        return await self.notification_repository.get_all_notifications()

    async def get_notification_by_id(self, id: int) -> Notification | None:
        return await self.notification_repository.get_notification_by_id(id)

    async def get_notifications_by_user(self, id_user: int) -> list[Notification] | Sequence[Notification]:
        return await self.notification_repository.get_notifications_by_user(id_user)

    async def create_notification(self, notification: Notification) -> Notification:
        return await self.notification_repository.create_notification(notification)
    
    async def delete_notification(self, notification: Notification) -> Notification | None:
        return await self.notification_repository.delete_notification(notification)
