from typing import Sequence
from core.db.session import session_factory, session as global_session
from sqlmodel import select

from modules.notification.domain.entity import Notification
from modules.notification.domain.repository.notification import NotificationRepository


class PostgresNotificationRepository(NotificationRepository):

    async def get_all_notifications(self) -> list[Notification] | Sequence[Notification]:
        query = select(Notification)

        async with session_factory() as session:
            result = await session.execute(query)
        return result.scalars().all()

    async def get_notification_by_id(self, id: int) -> Notification | None:
        query = select(Notification).where(Notification.id == id)

        async with session_factory() as session:
            result = await session.execute(query)
        return result.scalars().first()
    
    async def get_notifications_by_user(self, id_user: int) -> list[Notification] | Sequence[Notification]:
        query = select(Notification).where(Notification.user_id == id_user)

        async with session_factory() as session:
            result = await session.execute(query)
        return result.scalars().all()

    async def create_notification(self, notification: Notification) -> Notification:
        global_session.add(notification)
        await global_session.flush()
        return notification
    
    async def delete_notification(self, notification: Notification) -> Notification | None:
        await global_session.delete(notification)
        await global_session.flush()
        return notification
    