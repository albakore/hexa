"""
Tasks del módulo Invoicing - Input Adapter.

Estas funciones se registrarán automáticamente como tasks de Celery
a través del service_locator y el discovery automático.
"""
import time


def emit_invoice():
	"""
	Task para emitir factura.

	Esta función se ejecutará de forma asíncrona a través de Celery.
	Será registrada automáticamente como: "invoicing.emit_invoice"
	"""
	time.sleep(10)
	# Test: auto-reload feature
	return "Hola desde celery!!!"
