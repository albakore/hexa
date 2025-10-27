
from abc import ABC, abstractmethod
from typing import Sequence
from modules.notifications.domain.entity import Notification

class NotificationsRepository(ABC):
    @abstractmethod
    async def get_all_notifications(self) -> list[Notification] | Sequence[Notification]:
        ...

    @abstractmethod
    async def get_notifications_by_id(self, id: int) -> list[Notification] | Sequence[Notification]:
        ...

    @abstractmethod
    async def get_notifications_by_user(self, id_user: int) -> list[Notification] | Sequence[Notification]:
        ...    

    @abstractmethod
    async def create_notification(self, notification: Notification) -> Notification:
        ...