import importlib
import importlib.util
import os
from fastapi import APIRouter
import rich as r
from pathlib import Path

from sqlmodel import select

# Temporalmente comentado - será reemplazado por el nuevo sistema de módulos
# from modules.app_module.domain.entity.module import Module
# from core.db.session import session_factory

MODULE_REGISTRY: dict[str, dict] = {}


class ModuleSetup:
	"""Base class for module setup configuration"""
	name: str = ""
	token: str = ""
	description: str = ""


def get_modules_setup(folder_root_name: str = "modules"):
	"""Discover and load module setup configurations"""
	modules = []
	modules_path = Path(folder_root_name)
	
	if not modules_path.exists():
		return modules
	
	for module_dir in modules_path.iterdir():
		if module_dir.is_dir() and not module_dir.name.startswith('_'):
			setup_file = module_dir / "setup.py"
			if setup_file.exists():
				try:
					spec = importlib.util.spec_from_file_location(
						f"{module_dir.name}_setup", setup_file
					)
					module = importlib.util.module_from_spec(spec)
					spec.loader.exec_module(module)
					
					# Find ModuleSetup subclasses
					for attr_name in dir(module):
						attr = getattr(module, attr_name)
						if (isinstance(attr, type) and 
							issubclass(attr, ModuleSetup) and 
							attr != ModuleSetup):
							module_instance = attr()
							modules.append({
								'name': module_instance.name,
								'token': module_instance.token,
								'description': module_instance.description,
								'path': str(module_dir)
							})
							MODULE_REGISTRY[module_instance.token] = {
								'name': module_instance.name,
								'description': module_instance.description,
								'path': str(module_dir)
							}
				except Exception as e:
					print(f"Error loading module {module_dir.name}: {e}")
	
	return modules


async def sync_modules_to_db():
	"""Función temporal - no hace nada por ahora"""
	print("⚠️ Module sync temporalmente deshabilitado")
	pass


def get_all_system_modules():
	"""Get all registered system modules"""
	if not MODULE_REGISTRY:
		get_modules_setup()  # Auto-discover if not loaded
	return list(MODULE_REGISTRY.values())


system_modules = APIRouter(tags=["System"])


@system_modules.get("/modules")
def get_system_modules():
	return get_all_system_modules()