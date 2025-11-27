import asyncio
import importlib.util
import sys
from pathlib import Path

import typer
import uvicorn
from typer import Option

from shared.interfaces.service_protocols import YiqiServiceProtocol

sys.path.append(str(Path(__file__).resolve().parents[1]))
from sqlalchemy import text

from core.config.settings import env
from core.db.session import session_factory

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


@cmd.command("sync-db")
def sync_database(
	permissions: bool = Option(True, help="Sincronizar permisos"),
	modules: bool = Option(True, help="Sincronizar módulos"),
):
	"""
	Sincroniza permisos y módulos en la base de datos.

	Este comando descubre todos los módulos y permisos definidos en el código
	y los sincroniza con la base de datos.

	Ejemplos:
	  hexa sync-db                    # Sincroniza permisos y módulos
	  hexa sync-db --no-permissions   # Solo sincroniza módulos
	  hexa sync-db --no-modules       # Solo sincroniza permisos
	"""

	async def run_sync():
		typer.echo("\n🔄 Iniciando sincronización con la base de datos...")
		typer.echo("=" * 60)

		# Descubrir módulos primero (necesario para registrar permisos)
		from shared.interfaces.module_registry import ModuleRegistry
		from shared.interfaces.service_locator import service_locator

		ModuleRegistry().clear()
		service_locator.clear()

		typer.echo("\n📦 Descubriendo módulos...")
		from shared.interfaces.module_discovery import discover_modules

		discover_modules("modules", "module.py")
		typer.echo("✅ Módulos descubiertos\n")

		# Descubrir módulos setup (para MODULE_REGISTRY)
		from core.config.modules import get_modules_setup

		typer.echo("📦 Cargando configuraciones de módulos...")
		get_modules_setup("modules")
		typer.echo("✅ Configuraciones cargadas\n")

		# Descubrir y cargar permisos desde archivos permissions.py
		if permissions:
			typer.echo("🔍 Descubriendo archivos de permisos...")
			from shared.interfaces.module_discovery import discover_permissions

			discover_permissions("modules")
			typer.echo("")

		# Sincronizar permisos
		if permissions:
			typer.echo("🔐 Sincronizando permisos...")
			typer.echo("-" * 60)
			from core.fastapi.dependencies.permission import sync_permissions_to_db

			await sync_permissions_to_db()
			typer.echo("")

		# Sincronizar módulos
		if modules:
			typer.echo("📚 Sincronizando módulos...")
			typer.echo("-" * 60)
			from core.config.modules import sync_modules_to_db

			await sync_modules_to_db()
			typer.echo("")

		typer.echo("=" * 60)
		typer.echo("✨ Sincronización completada exitosamente\n")

	asyncio.run(run_sync())


@cmd.command("sync-with-yiqi-db")
def sync_with_yiqi_database(
	currencies: bool = Option(True, help="Sincronizar divisas"),
	services: bool = Option(True, help="Sincronizar servicios"),
	providers: bool = Option(True, help="Sincronizar proveedores"),
):
	async def run_sync():
		typer.echo("\n🔄 Iniciando sincronización de yiqi con la base de datos...")
		typer.echo("=" * 60)

		# Descubrir módulos primero (necesario para registrar permisos)
		from shared.interfaces.module_registry import ModuleRegistry
		from shared.interfaces.service_locator import service_locator

		ModuleRegistry().clear()
		service_locator.clear()

		typer.echo("\n📦 Descubriendo módulos...")
		from shared.interfaces.module_discovery import discover_modules

		discover_modules("modules", "module.py")
		typer.echo("✅ Módulos descubiertos\n")

		# Descubrir módulos setup (para MODULE_REGISTRY)
		from core.config.modules import get_modules_setup

		typer.echo("📦 Cargando configuraciones de módulos...")
		get_modules_setup("modules")
		typer.echo("✅ Configuraciones cargadas\n")

		yiqi_service: YiqiServiceProtocol = service_locator.get_service("yiqi_service")

		# Sincronizar currencies
		if currencies:
			typer.echo("🔍 Obteniendo currencies de yiqi...")
			from sqlmodel import select

			from modules.finance.domain.entity.currency import Currency

			currencies_data = await yiqi_service.get_currency_list(
				id_schema=env.YIQI_SCHEMA
			)

			async with session_factory() as session:
				try:
					created = 0
					updated = 0
					for currency_item in currencies_data:
						id_yiqi = currency_item.get("id")

						code = currency_item.get("MONE_NOMBRE", "")
						country = currency_item.get("PAIS_PAIS")

						if not code:
							continue

						# Buscar si ya existe la moneda
						stmt = select(Currency).where(Currency.code == code)
						result = await session.execute(stmt)
						existing_currency = result.scalars().first()

						if existing_currency:
							# Actualizar si existe
							existing_currency.name = code
							existing_currency.country = country
							session.add(existing_currency)
							updated += 1
						else:
							# Crear nueva si no existe
							new_currency = Currency(
								name=code,
								code=code,
								country=country,
							)
							session.add(new_currency)
							created += 1

					await session.commit()
					typer.echo(f"✅ Se sincronizaron {len(currencies_data)} currencies (Nuevas: {created}, Actualizadas: {updated})")
				except Exception as e:
					await session.rollback()
					typer.echo(f"❌ Error sincronizando currencies: {e}")
					raise
			typer.echo("")

		# Sincronizar servicios
		if services:
			typer.echo("🔍 Obteniendo servicios de yiqi...")
			from sqlmodel import select

			from modules.provider.domain.entity.purchase_invoice_service import (
				PurchaseInvoiceService,
			)

			services_data = await yiqi_service.get_services_list(
				id_schema=env.YIQI_SCHEMA
			)

			async with session_factory() as session:
				try:
					created = 0
					updated = 0
					for service_item in services_data:
						id_yiqi = service_item.get("id")

						name = service_item.get("SERV_SERVICIO", "")
						group = service_item.get("SERV_MARCA_DE_GASTOS")
						is_active = service_item.get("SERV_ACTIVO_PRO")

						# Solo sincronizar servicios activos o sin estado definido (None)
						# Filtrar solo los explícitamente inactivos ("N")
						if is_active == "N" or not name:
							continue

						# Buscar si ya existe el servicio
						stmt = select(PurchaseInvoiceService).where(
							PurchaseInvoiceService.id_yiqi_service == id_yiqi
						)
						result = await session.execute(stmt)
						existing_service = result.scalars().first()

						if existing_service:
							# Actualizar si existe
							existing_service.name = name
							existing_service.group = group
							session.add(existing_service)
							updated += 1
						else:
							# Crear nuevo si no existe
							new_service = PurchaseInvoiceService(
								name=name,
								group=group,
								id_yiqi_service=id_yiqi,
							)
							session.add(new_service)
							created += 1

					await session.commit()
					typer.echo(f"✅ Se sincronizaron {len(services_data)} servicios (Nuevos: {created}, Actualizados: {updated})")
				except Exception as e:
					await session.rollback()
					typer.echo(f"❌ Error sincronizando servicios: {e}")
					raise
			typer.echo("")

		# Sincronizar proveedores
		if providers:
			typer.echo("🔍 Obteniendo proveedores de yiqi...")
			from sqlmodel import select

			from modules.provider.domain.entity.provider import Provider

			providers_data = await yiqi_service.get_providers_list(
				id_schema=env.YIQI_SCHEMA
			)

			async with session_factory() as session:
				try:
					created = 0
					updated = 0
					for provider_item in providers_data:
						id_yiqi = provider_item.get("id")

						name = provider_item.get("CLIE_NOMBRE", "")
						currency = provider_item.get("CLIE_MONEDA")
						is_active_provider = provider_item.get("CLIE_ACTIVO_P") == "S"

						# Solo sincronizar proveedores activos
						if not is_active_provider or not name:
							continue

						# Buscar si ya existe el proveedor
						stmt = select(Provider).where(Provider.id_yiqi_provider == id_yiqi)
						result = await session.execute(stmt)
						existing_provider = result.scalars().first()

						if existing_provider:
							# Actualizar si existe
							existing_provider.name = name
							existing_provider.currency = currency
							session.add(existing_provider)
							updated += 1
						else:
							# Crear nuevo si no existe
							new_provider = Provider(
								name=name,
								currency=currency,
								id_yiqi_provider=id_yiqi,
							)
							session.add(new_provider)
							created += 1

					await session.commit()
					typer.echo(f"✅ Se sincronizaron {len(providers_data)} proveedores (Nuevos: {created}, Actualizados: {updated})")
				except Exception as e:
					await session.rollback()
					typer.echo(f"❌ Error sincronizando proveedores: {e}")
					raise
			typer.echo("")

		typer.echo("=" * 60)
		typer.echo("✨ Sincronización completada exitosamente\n")

	asyncio.run(run_sync())


if __name__ == "__main__":
	cmd()
