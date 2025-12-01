"""
Protocolo para servicios del módulo Notification.

Permite type checking y autocompletado sin crear dependencias directas
entre otros módulos.
"""

from typing import Any, Protocol, Self, TypedDict


class NotificationsTasksProtocol(Protocol):
	"""
	API pública de tasks de Celery del módulo Notifications.

	Estas tasks se ejecutan de forma asíncrona a través de Celery.
	Cada task tiene el método .delay() para ejecución asíncrona.
	"""

	def __call__(self) -> Self: ...
	def send_notification(self) -> str:
		"""
		Task para enviar notificación.

		Esta función se ejecutará de forma asíncrona a través de Celery.
		Nombre registrado: "notifications.send_notification"

		Usage:
			tasks = service_locator.get_service("notifications_tasks")
			tasks["send_notification"].delay()

		Returns:
			str: Mensaje de confirmación
		"""
		...


class EmailBasicInformation(TypedDict):
	to: list[str]
	subject: str


class NotificationCommandType(TypedDict):
	notification: dict[str, Any]
	sender: str


class EmailNotificationCommandType(TypedDict):
	template_name: str
	notification: EmailBasicInformation
	data_injection: dict


class NotificationServiceProtocol(Protocol):
	def __call__(self) -> Self: ...

	async def get_all_notifications(self) -> list[Any]: ...

	async def get_notification_by_id(self, id: int) -> Any: ...

	async def create_notification(self, command: Any) -> Any | None: ...
	async def delete_notification(self, id: int) -> Any | None: ...

	async def send_notification(self, command: NotificationCommandType) -> None: ...
	async def send_email_notification(
		self, command: EmailNotificationCommandType
	) -> None: ...


class EmailTemplateServiceProtocol(Protocol):
	def __call__(self) -> Self: ...

	async def get_all_email_templates(self) -> list[Any]: ...

	async def get_email_template_by_id(self, id: int) -> Any: ...

	async def get_email_template_by_name(self, name: str) -> Any: ...

	async def get_email_template_by_module(self, module: str) -> Any: ...

	async def save_email_template(self, template: Any) -> Any: ...

	async def edit_email_template(self, id: int, command: Any) -> Any: ...

	async def delete_email_template(self, id: int) -> None: ...
