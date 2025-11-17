"""
Sistema simplificado de auto-registro de tareas de celery usando service_locator.

Este módulo descubre automáticamente todas las tasks registradas en el service_locator
y las registra en una única instancia de Celery.

Soporta tasks asíncronas usando asyncio.
"""

import asyncio
import inspect
from celery import Celery
from core.celery import celery_app


def register_celery_tasks() -> int:
	"""
	Registra todas las tasks descubiertas desde service_locator en celery_app.

	Las tasks deben estar registradas en service_locator con nombres que terminen en "_tasks".
	Cada servicio de tasks puede tener dos formatos:

	Formato 1 - Simple (solo funciones):
	{
		"task_name": callable_function,
		...
	}

	Formato 2 - Con configuración (diccionario con task y config):
	{
		"task_name": {
			"task": callable_function,
			"config": {
				"autoretry_for": (Exception,),
				"retry_kwargs": {"max_retries": 5},
				"retry_backoff": True,
				"retry_backoff_max": 600,
				"retry_jitter": True,
				...
			}
		},
		...
	}

	Returns:
		int: Número de tasks registradas
	"""
	from shared.interfaces.service_locator import service_locator

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

		for task_name, task_data in task_dict.items():
			# Determinar si es formato simple o con configuración
			if callable(task_data):
				# Formato simple: solo la función
				task_func = task_data
				task_config = {}
			elif isinstance(task_data, dict) and "task" in task_data:
				# Formato con configuración
				task_func = task_data["task"]
				task_config = task_data.get("config", {})
			else:
				print(f"  ⚠️  Skipping {module_name}.{task_name}: invalid format")
				continue

			if not callable(task_func):
				print(f"  ⚠️  Skipping {module_name}.{task_name}: task is not callable")
				continue

			# Si la función es async, envolverla en un wrapper síncrono
			if inspect.iscoroutinefunction(task_func):
				original_func = task_func

				def make_sync_wrapper(async_func):
					def sync_wrapper(*args, **kwargs):
						# Verificar si ya hay un event loop corriendo
						try:
							asyncio.get_running_loop()
							# Si llegamos aquí, hay un loop corriendo, lo cual no debería pasar en Celery
							raise RuntimeError(
								"Cannot run async task, event loop already running"
							)
						except RuntimeError:
							# No hay loop corriendo, esto es lo esperado en Celery worker
							pass

						# Intentar obtener el loop actual
						try:
							loop = asyncio.get_event_loop()
							# Si el loop está cerrado o viene del fork, crear uno nuevo
							if loop.is_closed():
								loop = asyncio.new_event_loop()
								asyncio.set_event_loop(loop)
						except RuntimeError:
							# No existe loop, crear uno nuevo
							loop = asyncio.new_event_loop()
							asyncio.set_event_loop(loop)

						# Ejecutar la función async
						try:
							return loop.run_until_complete(async_func(*args, **kwargs))
						finally:
							# Limpiar tareas pendientes pero NO cerrar el loop
							# Esto permite reusar el loop en la siguiente tarea del mismo worker
							try:
								pending = asyncio.all_tasks(loop)
								if pending:
									for task in pending:
										task.cancel()
									# Ejecutar un tick del loop para procesar cancelaciones
									if pending:
										loop.run_until_complete(asyncio.sleep(0))
							except Exception:
								pass

					sync_wrapper.__name__ = async_func.__name__
					sync_wrapper.__doc__ = async_func.__doc__
					return sync_wrapper

				task_func = make_sync_wrapper(original_func)
				is_async = True
			else:
				is_async = False

			# Registrar con nombre descriptivo y configuración
			full_task_name = f"{module_name}.{task_name}"
			celery_app.task(name=full_task_name, **task_config)(task_func)
			registered_count += 1

			# Mostrar configuración si existe
			async_marker = " [async]" if is_async else ""
			if task_config:
				config_info = ", ".join([f"{k}={v}" for k, v in task_config.items()])
				print(f"  ✓ Registered: {full_task_name}{async_marker} ({config_info})")
			else:
				print(f"  ✓ Registered: {full_task_name}{async_marker}")

	print(f"\n✅ Total {registered_count} tasks registered in Celery worker\n")
	return registered_count


def create_celery_worker() -> Celery:
	"""
	Crea el worker de Celery con todas las tasks descubiertas desde service_locator.

	IMPORTANTE: Esta función espera que los módulos YA hayan sido descubiertos
	y que las tasks estén registradas en service_locator.

	Returns:
		Celery: Instancia configurada de Celery con todas las tasks registradas
	"""
	register_celery_tasks()
	return celery_app


def get_celery_app() -> Celery:
	"""
	Retorna la instancia de celery_app SIN registrar tasks.

	Usar esta función cuando se necesite la instancia de Celery
	ANTES de que los módulos sean descubiertos (ej: en FastAPI startup).

	Returns:
		Celery: Instancia de Celery
	"""
	return celery_app
