"""
Tasks del módulo Notifications - Input Adapter.

Estas funciones se registrarán automáticamente como tasks de Celery
a través del service_locator y el discovery automático.
"""


def send_notification():
	"""
	Task para enviar notificación.

	Esta función se ejecutará de forma asíncrona a través de Celery.
	Será registrada automáticamente como: "notifications.send_notification"
	"""
	return "Esto es una notificacion"
