from dataclasses import dataclass

from modules.notification.domain.command import CreateNotificationCommand
from modules.notification.domain.repository.notification import NotificationRepository
from modules.notification.domain.usecase.notification import NotificationUseCaseFactory


@dataclass
class NotificationService:
    
    notification_repository : NotificationRepository

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

    
    #TODO: agregar envíos de notificaciones por email y probarlas
    # def send_notification_email(self, id: int):
    
    # def get_notifications_by_user(self, id_user: int):
    #     #TODO: Implement this use case in the factory and usecase classes
    #     notification = self.usecase.get_notifications_by_user(id_user)
    #     return notification
    