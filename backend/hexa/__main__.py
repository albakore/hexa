import asyncio
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


if __name__ == "__main__":
	cmd()
