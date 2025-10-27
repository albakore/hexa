"""
Sistema simplificado de auto-registro de tareas de celery usando service_locator.

Este módulo descubre automáticamente todas las tasks registradas en el service_locator
y las registra en una única instancia de Celery.
"""

from celery import Celery
from core.config.settings import env


def create_celery_worker() -> Celery:
	"""
	Crea el worker de Celery con todas las tasks descubiertas desde service_locator.

	Las tasks deben estar registradas en service_locator con nombres que terminen en "_tasks".
	Cada servicio de tasks debe ser un diccionario con el formato:
	{
		"task_name": callable_function,
		...
	}

	Returns:
		Celery: Instancia configurada de Celery con todas las tasks registradas
	"""
	from shared.interfaces.service_locator import service_locator

	# Crear la aplicación maestra de Celery
	app = Celery(
		"hexa_worker",
		broker=env.RABBITMQ_URL,
		backend=env.REDIS_URL,
	)

	# Obtener todos los servicios que terminan en "_tasks"
	task_services = {
		name: service
		for name, service in service_locator._services.items()
		if name.endswith("_tasks")
	}

	print(f"\n📦 Discovered {len(task_services)} task services from service_locator")

	# Registrar cada función como task de Celery
	registered_count = 0
	for service_name, task_dict in task_services.items():
		# Extraer nombre del módulo: "invoicing_tasks" -> "invoicing"
		module_name = service_name.replace("_tasks", "")

		if not isinstance(task_dict, dict):
			print(f"  ⚠️  Skipping {service_name}: not a dict")
			continue

		for task_name, task_func in task_dict.items():
			if not callable(task_func):
				print(f"  ⚠️  Skipping {module_name}.{task_name}: not callable")
				continue

			# Registrar con nombre descriptivo: "invoicing.emit_invoice"
			full_task_name = f"{module_name}.{task_name}"
			app.task(name=full_task_name)(task_func)
			registered_count += 1
			print(f"  ✓ Registered: {full_task_name}")

	print(f"\n✅ Total {registered_count} tasks registered in Celery worker\n")

	return app
