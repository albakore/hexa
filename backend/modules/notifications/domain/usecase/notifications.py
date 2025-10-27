from dataclasses import dataclass
from typing import Sequence
from core.db.transactional import Transactional
from modules.notifications.domain.command import CreateNotificationCommand
from modules.notifications.domain.entity.notifications import Notification
from modules.notifications.domain.repository.notifications import NotificationsRepository

class UseCase:
    ...

@dataclass
class GetAllNotifications(UseCase):

    notification_repository : NotificationsRepository

    async def __call__(self) -> list[Notification] | Sequence[Notification]:
        notifications = await self.notification_repository.get_all_notifications()
        return notifications

@dataclass
class GetNotificationById(UseCase):

    notification_repository : NotificationsRepository

    async def __call__(self,id: int) -> list[Notification] | Sequence[Notification]:
        notifications = await self.notification_repository.get_notifications_by_id(id)
        return notifications

@dataclass
class CreateNotification(UseCase):

    notification_repository : NotificationsRepository

    @Transactional()
    async def __call__(self, command: CreateNotificationCommand) -> Notification:
        notification = Notification.model_validate(command)
        new_notification = await self.notification_repository.create_notification(notification)
        return new_notification

@dataclass
class NotificationsUseCaseFactory:

    notification_repository : NotificationsRepository

    def __post_init__(self):
        self.get_all_notifications = GetAllNotifications(self.notification_repository)
        self.get_notification_by_id = GetNotificationById(self.notification_repository)
        self.create_notification = CreateNotification(self.notification_repository)