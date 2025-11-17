"""
Tasks del módulo Notification - Input Adapter.

Estas funciones se registrarán automáticamente como tasks de Celery
a través del service_locator y el discovery automático.
"""

import uuid
from core.db.session import reset_session_context, set_session_context
from modules.notification.container import NotificationContainer


async def send_notification_tasks(notification_content: dict):
	"""
	Task para enviar notificación.

	Esta función se ejecutará de forma asíncrona a través de Celery.
	Será registrada automáticamente como: "notification.send_notification"
	return "Esto es una notificacion"
	"""
	try:
		notification_service = NotificationContainer().service()

		session_uuid = uuid.uuid4()
		context = set_session_context(str(session_uuid))

		await notification_service.send_notification(notification_content)

	finally:
		reset_session_context(context)
