"""
Tasks del módulo YiqiERP - Input Adapter.

Estas funciones se registrarán automáticamente como tasks de Celery
a través del service_locator y el discovery automático.
"""


def emit_invoice(data):
	"""
	Task para emitir factura al ERP externo Yiqi.

	Esta función se ejecutará de forma asíncrona a través de Celery.
	Será registrada automáticamente como: "yiqi_erp.emit_invoice"

	Args:
		data: Datos de la factura a emitir
	"""
	print(data)
	return f"YIQI ERP: Hola desde celery!!!"
