import asyncio
from celery import Celery
import typer
import uvicorn
import sys
from pathlib import Path
import importlib.util

sys.path.append(str(Path(__file__).resolve().parents[1]))
from core.db.session import session, session_factory
from core.config.settings import env
from sqlalchemy import text

# Configuración del CLI principal
cmd = typer.Typer(rich_markup_mode="rich", help="Gestor del proyecto hexagonal")


# Comando para la API
@cmd.command()
def api(dev: bool = False):
	"""Inicia el servidor FastAPI"""
	verify_project_structure()
	port = 8000
	uvicorn.run(
		"core.fastapi.server:app",
		host="0.0.0.0",
		port=port,
		reload=dev,
		root_path=env.BACKEND_PATH,
	)


@cmd.command("delete-alembic-version")
def delete_alembic_version():
	"""Borra ultima version guardada de la migracion de alembic"""

	async def delete_version():
		async with session_factory() as s:
			await s.execute(text("DELETE FROM alembic_version"))
			await s.commit()
			typer.echo("✅ Se eliminó el registro de la tabla alembic_version.")

	asyncio.run(delete_version())


@cmd.command("makeuser")
def create_user():
	"""Crea un usuario"""
	...


# Función de verificación común
def verify_project_structure():
	if not importlib.util.find_spec("core.fastapi.server"):
		typer.echo(
			"Error: No se encontró 'core.fastapi.server'. ¿Estás en el root del proyecto?",
			err=True,
		)
		sys.exit(1)


@cmd.command("celery-apps")
def run_celery():
	"""Inicia el worker de Celery con todas las tasks descubiertas desde service_locator"""
	# IMPORTANTE: Limpiar registros antes de descubrir módulos
	# Esto es necesario para cuando watchfiles reinicia el worker
	from shared.interfaces.module_registry import ModuleRegistry
	from shared.interfaces.service_locator import service_locator

	ModuleRegistry().clear()
	service_locator.clear()

	# Descubrir y registrar módulos ANTES de crear el worker
	# Esto inicializa el service_locator con todos los servicios (incluyendo tasks)
	from shared.interfaces.module_discovery import discover_modules

	print("🔍 Discovering and registering modules...")
	discover_modules("modules", "module.py")
	print("✅ Modules registered\n")

	# Ahora crear el worker (service_locator ya tiene las tasks registradas)
	from core.celery.discovery import create_celery_worker

	app = create_celery_worker()
	app.worker_main(["worker", "--loglevel=INFO"])


@cmd.command("test-celery")
def test_celery():
	"""Prueba ejecutar tasks de Celery"""
	from shared.interfaces.service_locator import service_locator

	# Obtener tasks desde service_locator
	invoicing_tasks = service_locator.get_service("invoicing_tasks")
	yiqi_tasks = service_locator.get_service("yiqi_erp_tasks")
	notification_tasks = service_locator.get_service("notifications_tasks")

	# Ejecutar tasks de prueba
	if invoicing_tasks:
		invoicing_tasks["emit_invoice"].delay()
		print("✅ Task de invoicing enviada")

	if yiqi_tasks:
		yiqi_tasks["emit_invoice"].delay({"test": "data"})
		print("✅ Task de yiqi_erp enviada")

	if notification_tasks:
		notification_tasks["send_notification"].delay()
		print("✅ Task de notifications enviada")

	print("\n📤 Se enviaron todas las tareas de prueba")


if __name__ == "__main__":
	cmd()
