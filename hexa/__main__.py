import typer
import uvicorn
import sys
from pathlib import Path
import importlib.util

sys.path.append(str(Path(__file__).resolve().parents[1]))

cmd = typer.Typer(rich_markup_mode="rich")


@cmd.command()
def api(dev: bool = False):
	if not importlib.util.find_spec("app.server"):
		print("No se encontró 'app.server'. ¿Estás en el root del proyecto, salame?")
		sys.exit(1)

	port = 8000 if dev else 8080
	reload = dev
	uvicorn.run("app.server:app",host="0.0.0.0",port=port,reload=reload)

@cmd.command()
def makemigrations():
	print("makemigrations!")

@cmd.command()
def migrate():
	print("migrate!")

def main(dev: bool = False):
	"""Este es el comando por defecto."""
	if not importlib.util.find_spec("app.server"):
		print("No se encontró 'app.server'. ¿Estás en el root del proyecto, salame?")
		sys.exit(1)

	port = 8000 if dev else 8080
	reload = dev
	uvicorn.run("app.server:app",host="0.0.0.0",port=port,reload=reload)


# def main():
# 	print("hola mundo")

if __name__ == "__main__":
	typer.run(main)