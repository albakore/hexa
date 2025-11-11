from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends

from modules.notification.adapter.input.api.v1.request import (
	CreateNotificationRequest,
	SendNotificationRequest,
)
from modules.notification.application.service.notification import NotificationService
from modules.notification.container import NotificationContainer


notifications_router = APIRouter()


@notifications_router.get("")
@inject
async def get_all_notifications(
	notifications_service: NotificationService = Depends(
		Provide[NotificationContainer.service]
	),
):
	notifications = await notifications_service.get_all_notifications()
	return notifications


@notifications_router.post("")
@inject
async def create_notification(
	notification: CreateNotificationRequest,
	notifications_service: NotificationService = Depends(
		Provide[NotificationContainer.service]
	),
):
	new_notification = await notifications_service.create_notification(notification)
	return new_notification


@notifications_router.post("/send")
@inject
async def send_notification(
	notification: SendNotificationRequest,
	notifications_service: NotificationService = Depends(
		Provide[NotificationContainer.service]
	),
):
	await notifications_service.send_notification(notification)
	return {"status": "OK"}
