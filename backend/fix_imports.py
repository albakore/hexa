#!/usr/bin/env python3
"""
Script para actualizar importaciones obsoletas de 'app.' a 'modules.'
"""

import os
import re
from pathlib import Path


def fix_imports_in_file(file_path: Path):
	"""Actualizar importaciones en un archivo específico"""
	try:
		with open(file_path, "r", encoding="utf-8") as f:
			content = f.read()

		original_content = content

		# Patrones de reemplazo
		replacements = [
			# Importaciones específicas de módulos
			(r"from app\.auth\.", "from modules.auth."),
			(r"from app\.user\.", "from modules.user."),
			(r"from app\.rbac\.", "from modules.rbac."),
			(r"from app\.user_relationships\.", "from modules.user_relationships."),
			(r"from app\.module\.", "from modules.app_module."),
			# Importaciones de container
			(
				r"from app\.container import SystemContainer",
				"# # from app.container import SystemContainer  # DEPRECATED  # DEPRECATED",
			),
			# Importaciones de modelos
			(r"from app\.models", "# # from app.models  # DEPRECATED  # DEPRECATED"),
			# Imports de app genéricos
			(r"import app\.", "import modules."),
		]

		# Aplicar reemplazos
		for pattern, replacement in replacements:
			content = re.sub(pattern, replacement, content)

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

	# Buscar archivos Python
	python_files = list(backend_dir.rglob("*.py"))

	fixed_count = 0
	total_count = len(python_files)

	print(f"🔍 Scanning {total_count} Python files...")

	for file_path in python_files:
		# Saltar archivos en directorios específicos
		if any(part in str(file_path) for part in [".venv", "__pycache__", ".git"]):
			continue

		if fix_imports_in_file(file_path):
			fixed_count += 1

	print(f"\n📊 Summary:")
	print(f"   Total files: {total_count}")
	print(f"   Fixed files: {fixed_count}")
	print(f"   Unchanged: {total_count - fixed_count}")


if __name__ == "__main__":
	main()
