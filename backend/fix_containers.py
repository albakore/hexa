#!/usr/bin/env python3
"""
Script para actualizar referencias a SystemContainer obsoleto
"""

import os
import re
from pathlib import Path


def fix_container_references(file_path: Path):
	"""Actualizar referencias a containers en un archivo específico"""
	try:
		with open(file_path, "r", encoding="utf-8") as f:
			content = f.read()

		original_content = content

		# Patrones de reemplazo para SystemContainer
		replacements = [
			# Imports de dependency injection
			(
				r"from dependency_injector\.wiring import Provide, inject",
				"# from dependency_injector.wiring import Provide, inject  # DEPRECATED",
			),
			(r"@inject", "# @inject  # DEPRECATED"),
			# Referencias específicas a SystemContainer
			(
				r"Depends\(Provide\[SystemContainer\.auth\.service\]\)",
				"None  # TODO: Use service_locator",
			),
			(
				r"Depends\(Provide\[SystemContainer\.auth\.jwt_service\]\)",
				"None  # TODO: Use service_locator",
			),
			(
				r"Depends\(Provide\[SystemContainer\.user\.service\]\)",
				"None  # TODO: Use service_locator",
			),
			(
				r"Depends\(Provide\[SystemContainer\.rbac\.role_service\]\)",
				"None  # TODO: Use service_locator",
			),
			(
				r"Depends\(Provide\[SystemContainer\.rbac\.permission_service\]\)",
				"None  # TODO: Use service_locator",
			),
			(
				r"Depends\(Provide\[SystemContainer\.app_module\.service\]\)",
				"None  # TODO: Use service_locator",
			),
			(
				r"Depends\(Provide\[SystemContainer\.user_relationship\.service\]\)",
				"None  # TODO: Use service_locator",
			),
			# Parámetros de función con SystemContainer
			(
				r"(\w+): (\w+) = Depends\(Provide\[SystemContainer\.\w+\.\w+\]\)",
				r"# \1: \2 = None  # TODO: Use service_locator",
			),
		]

		# Aplicar reemplazos
		for pattern, replacement in replacements:
			content = re.sub(pattern, replacement, content)

		# Agregar import de service_locator si no existe y se necesita
		if "service_locator" not in content and "TODO: Use service_locator" in content:
			# Buscar línea de imports
			lines = content.split("\n")
			import_index = -1
			for i, line in enumerate(lines):
				if line.startswith("from ") or line.startswith("import "):
					import_index = i

			if import_index >= 0:
				lines.insert(
					import_index + 1,
					"from shared.interfaces.service_locator import service_locator",
				)
				content = "\n".join(lines)

		# Solo escribir si hubo cambios
		if content != original_content:
			with open(file_path, "w", encoding="utf-8") as f:
				f.write(content)
			print(f"✅ Fixed containers: {file_path}")
			return True

		return False

	except Exception as e:
		print(f"❌ Error fixing {file_path}: {e}")
		return False


def main():
	"""Función principal"""
	backend_dir = Path(".")

	# Buscar archivos Python en modules/
	python_files = list(backend_dir.glob("modules/**/*.py"))

	fixed_count = 0
	total_count = len(python_files)

	print(f"🔍 Scanning {total_count} Python files in modules/...")

	for file_path in python_files:
		if fix_container_references(file_path):
			fixed_count += 1

	print(f"\n📊 Summary:")
	print(f"   Total files: {total_count}")
	print(f"   Fixed files: {fixed_count}")
	print(f"   Unchanged: {total_count - fixed_count}")


if __name__ == "__main__":
	main()
