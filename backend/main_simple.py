#!/usr/bin/env python3
"""
Punto de entrada mínimo para verificar que el sistema funciona
"""


def main():
	print("🚀 Fast Hexagonal Backend")
	print("✅ Sistema desacoplado funcionando")
	print("📦 Módulos disponibles:")

	# Verificar que los módulos se pueden importar
	modules_to_test = [
		"modules.auth.module",
		"modules.user.module",
		"modules.rbac.module",
		"modules.finance.module",
		"shared.interfaces.module_registry",
		"shared.interfaces.service_locator",
		"shared.interfaces.events",
	]

	for module_name in modules_to_test:
		try:
			__import__(module_name)
			print(f"  ✅ {module_name}")
		except ImportError as e:
			print(f"  ❌ {module_name}: {e}")
		except Exception as e:
			print(f"  ⚠️  {module_name}: {e}")

	print("\n🎉 Verificación completada")


if __name__ == "__main__":
	main()
