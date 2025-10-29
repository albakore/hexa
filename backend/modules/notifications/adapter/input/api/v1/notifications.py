from dependency_injector.wiring import inject,Provide
from fastapi import APIRouter, Depends

from modules.notifications.adapter.input.api.v1.request import CreateNotificationRequest
from modules.notifications.application.service.notifications import NotificationService
from modules.notifications.container import NotificationsContainer


notifications_router = APIRouter()

@notifications_router.get("")
@inject
async def get_all_notifications(
    notifications_service : NotificationService = Depends(Provide[NotificationsContainer.service]),
):
    notifications = await notifications_service.get_all_notifications()
    return notifications

@notifications_router.post("")
@inject
async def create_notification(
    notification: CreateNotificationRequest,
    notifications_service : NotificationService = Depends(Provide[NotificationsContainer.service]),
):
    new_notification = await notifications_service.create_notification(notification)
    return new_notification
