
import importlib
import importlib.util
import os
from fastapi import APIRouter
import rich as r
from pathlib import Path

from sqlmodel import select

from app.module.domain.entity.module import Module
from core.db.session import session_factory

MODULE_REGISTRY : dict[str, dict] = {}

class ModuleSetup:
	name: str | None = None  # puede sobrescribirse
	token: str
	description: str| None = None

	@classmethod
	def __init_subclass__(cls):
		cls._name = cls.name or cls.__name__.lower()

		MODULE_REGISTRY[cls._name] = {
			"name": cls.name,
			"token": cls.token,
			"description" : cls.description
		}

	@classmethod
	def list_permissions(cls):
		return [item for attr, item in MODULE_REGISTRY.items()]


def get_modules_setup(folder_root_name : str = "modules") :
	configs = []
	for subdir in Path(folder_root_name).iterdir():
		# print(Path(subdir).name)
		if subdir.is_dir() and not subdir.name.startswith("_"):
			setup_route = subdir / "setup.py"

			if setup_route.is_file():
				module_name = "setup"
				module_route = ".".join([folder_root_name,subdir.name,module_name])
				importlib.import_module(module_route)

			print(f"❌ Modulo [{subdir.name}] no existe 'setup.py'")
	return configs


async def sync_modules_to_db():
	"""
	Sincroniza los modulos definidos en código con la base de datos.
	"""
	async with session_factory() as session:
		try:
			for name, item in MODULE_REGISTRY.items():
				result = await session.execute(select(Module).where(Module.token == item['token']))
				db_module = result.scalars().first()

				if db_module:
					if db_module.description != item['description'] or db_module.name != item['name']:
						if db_module.description != item['description']:
							db_module.description = item['description']
						if db_module.name != item['name']:
							db_module.name = item['name']
						session.add(db_module)
						print(f"📝 Actualizado modulo: {item['name']}")
				else:
					session.add(Module(name=item['name'], token=item['token'], description=item.get('description',None)))
					print(f"🆕 Insertado modulo: {item['name']}")

			await session.commit()
			print("✅ Modulos sincronizados en base de datos")
		except Exception as e:
			print("❌ Hubo un error al sincronizar los modulos:", e)


def get_all_system_modules():
	values = MODULE_REGISTRY.values()
	return list(values)


system_modules = APIRouter(tags=["System"])

@system_modules.get("/modules")
def get_system_modules():
	return get_all_system_modules()