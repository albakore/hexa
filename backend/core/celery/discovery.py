"""
Sistema simplificado de auto-registro
"""

from pathlib import Path
import importlib.util
from types import ModuleType
from typing import Any

from celery import Celery


def eval_module_is_dir(path: Path) -> bool:
	return path.is_dir() and not path.name.startswith("_")


def module_exists(path: Path) -> bool:
	return path.exists()


def convert_path_to_pythonpath(path: Path) -> str:
	return str(path.with_suffix("")).replace("/", ".")


def import_python_module(python_path: str) -> ModuleType | None:
	try:
		print(python_path)
		return importlib.import_module(python_path)
	except ImportError as e:
		print("❌ Error import:", e, "path:", e.path)
		return None


def extract_attributes_from_module(module: ModuleType) -> list[str]:
	return dir(module)


def is_subclass_of(subclass_attribute: Any, parent_class: type) -> bool:
	return (
		isinstance(subclass_attribute, parent_class)
		# and issubclass(subclass_attribute, parent_class)
		and subclass_attribute != parent_class
	)


def merge_celery_tasks(master_app: Celery, other_apps: list[Celery]):
	for app in other_apps:
		for name, task in app.tasks.items():
			if name.startswith("celery.") or name in master_app.tasks:
				continue
			master_app.tasks[name] = task
	print(app.tasks)


def discover_celery_apps(root_dir: str):
	"""Busca y devuelve una lista de instancias de celery"""

	base_path = Path(root_dir)
	celery_count = 0
	apps: list[Celery] = []

	for module_dir in base_path.iterdir():
		if not eval_module_is_dir(module_dir):
			continue

		task_folder = module_dir / "adapter" / "input" / "tasks"
		if not task_folder.exists():
			continue

		for task_file in task_folder.glob("*.py"):
			if task_file.name.startswith("_"):
				continue

		try:
			python_path = convert_path_to_pythonpath(task_file)
		except ValueError as e:
			# fallback si estás ejecutando desde otro lugar
			print("ERROR:", e)
			python_path = convert_path_to_pythonpath(
				task_file.relative_to(base_path.parent)
			)

		module = import_python_module(python_path)
		if not module:
			continue
		module_attributes = extract_attributes_from_module(module)
		for attribute in module_attributes:
			module_subclass: Celery = getattr(module, attribute)
			if is_subclass_of(module_subclass, Celery):
				apps.append(module_subclass)
				celery_count += 1

	print(f"📦 Total {celery_count} celery instances")
	return apps
