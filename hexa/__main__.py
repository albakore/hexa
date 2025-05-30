import typer
import uvicorn
import sys
from pathlib import Path
import importlib.util
sys.path.append(str(Path(__file__).resolve().parents[1]))
from core.db.session import session

from app.models import create_tables, drop_tables

# Configuración del CLI principal
cmd = typer.Typer(rich_markup_mode="rich", help="Gestor del proyecto hexagonal")

# Comando para la API
@cmd.command()
def api(dev: bool = False):
    """Inicia el servidor FastAPI"""
    verify_project_structure()
    port = 8000 if dev else 8080
    uvicorn.run("app.server:app", host="0.0.0.0", port=port, reload=dev)

# Comandos para la base de datos
db_app = typer.Typer(help="Comandos para gestión de la base de datos")
cmd.add_typer(db_app, name="db")

@db_app.command("create-tables")
def create_all(verbose: bool = True):
    """Crea todas las tablas en la base de datos"""
    create_tables(session.bind)
    if verbose:
        typer.echo("✅ Tablas creadas exitosamente")

@db_app.command("drop-tables")
def drop_all(verbose: bool = True):
    """Elimina todas las tablas de la base de datos"""
    drop_tables(session.bind)
    if verbose:
        typer.echo("🗑️ Tablas eliminadas exitosamente")

# Comandos para migraciones
migrations_app = typer.Typer(help="Comandos para migraciones de base de datos")
cmd.add_typer(migrations_app, name="migrations")

@migrations_app.command("make")
def makemigrations(message: str = typer.Option(..., "--message", "-m")):
    """Crea nuevas migraciones"""
    # Implementación real con Alembic
    typer.echo(f"📝 Creando migración: {message}")

@migrations_app.command("apply")
def migrate():
    """Aplica migraciones pendientes"""
    typer.echo("🔄 Aplicando migraciones...")

# Función de verificación común
def verify_project_structure():
    if not importlib.util.find_spec("app.server"):
        typer.echo("Error: No se encontró 'app.server'. ¿Estás en el root del proyecto?", err=True)
        sys.exit(1)

if __name__ == "__main__":
    cmd()