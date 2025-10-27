from dataclasses import dataclass

from modules.notifications.domain.command import CreateNotificationCommand
from modules.notifications.domain.repository.notifications import NotificationsRepository
from modules.notifications.domain.usecase.notifications import NotificationsUseCaseFactory

@dataclass
class NotificationService:
    
    notification_repository : NotificationsRepository

    def __post_init__(self):
        self.usecase = NotificationsUseCaseFactory(self.notification_repository)

    def get_all_notifications(self):
        notifications = self.usecase.get_all_notifications()
        return notifications
    
    def get_notification_by_id(self, id: int):
        notification = self.usecase.get_notification_by_id(id)
        return notification
    
    def create_notification(self, command : CreateNotificationCommand):
        new_notification = self.usecase.create_notification(command)
        return new_notification
    
    # def get_notifications_by_user(self, id_user: int):
    #     #TODO: Implement this use case in the factory and usecase classes
    #     notification = self.usecase.get_notifications_by_user(id_user)
    #     return notification