
from dataclasses import dataclass
from typing import Sequence
from modules.notifications.domain.entity import Notification
from modules.notifications.domain.repository.notifications import NotificationsRepository

@dataclass
class NotificationRepositoryAdapter(NotificationsRepository):
    notification_repository: NotificationsRepository

    async def get_all_notifications(self) -> list[Notification] | Sequence[Notification]:
        return await self.notification_repository.get_all_notifications()

    async def get_notifications_by_id(self, id: int) -> list[Notification] | Sequence[Notification]:
        return await self.notification_repository.get_notifications_by_id(id)

    async def get_notifications_by_user(self, id_user: int) -> list[Notification] | Sequence[Notification]:
        return await self.notification_repository.get_notifications_by_user(id_user)

    async def create_notification(self, notification: Notification) -> Notification:
        return await self.notification_repository.create_notification(notification)


