#!/usr/bin/env python3
"""
Script para corregir todos los controladores de input API
"""

import os
import re
from pathlib import Path


def fix_controller_file(file_path: Path):
	"""Corregir un archivo de controlador específico"""
	try:
		with open(file_path, "r", encoding="utf-8") as f:
			content = f.read()

		original_content = content

		# Patrones de reemplazo
		replacements = [
			# Imports obsoletos
			(r"from dependency_injector\.wiring import.*\n", ""),
			(r"from modules\.container import.*\n", ""),
			(r"# from dependency_injector\.wiring import.*\n", ""),
			# Agregar import de service_locator si no existe
			(
				r"(from fastapi import.*\n)",
				r"\1from shared.interfaces.service_locator import service_locator\n",
			),
			# Remover decoradores obsoletos
			(r"@inject.*\n", ""),
			(r"# @inject.*\n", ""),
			# Remover parámetros de dependency injection
			(r"(\w+): (\w+Service) = Depends\([^)]+\),?\n?", ""),
			(r"(\w+): (\w+Service) = None  # TODO: Use service_locator,?\n?", ""),
		]

		# Aplicar reemplazos básicos
		for pattern, replacement in replacements:
			content = re.sub(pattern, replacement, content)

		# Limpiar líneas vacías múltiples
		content = re.sub(r"\n\n\n+", "\n\n", content)

		# Solo escribir si hubo cambios
		if content != original_content:
			with open(file_path, "w", encoding="utf-8") as f:
				f.write(content)
			print(f"✅ Fixed: {file_path}")
			return True

		return False

	except Exception as e:
		print(f"❌ Error fixing {file_path}: {e}")
		return False


def main():
	"""Función principal"""
	backend_dir = Path(".")

	# Archivos específicos a corregir
	files_to_fix = [
		"modules/user_relationships/adapter/input/api/v1/user_relationship.py",
		"modules/yiqi_erp/adapter/input/api/v1/yiqi_erp.py",
		"modules/provider/adapter/input/api/v1/draft_invoice.py",
		"modules/provider/adapter/input/api/v1/provider.py",
		"modules/user/adapter/input/api/v1/user.py",
	]

	fixed_count = 0

	for file_path_str in files_to_fix:
		file_path = backend_dir / file_path_str
		if file_path.exists():
			if fix_controller_file(file_path):
				fixed_count += 1
		else:
			print(f"⚠️  File not found: {file_path}")

	print(f"\n📊 Fixed {fixed_count} controller files")


if __name__ == "__main__":
	main()
