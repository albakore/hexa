#!/usr/bin/env python3
"""
Test básico del sistema desacoplado
"""


def test_imports():
	"""Probar que las importaciones básicas funcionan"""
	print("🧪 Testing system imports...")

	try:
		# Test shared interfaces
		from shared.interfaces.module_registry import ModuleRegistry, module_registry

		print("✅ ModuleRegistry imported")

		from shared.interfaces.service_locator import ServiceLocator, service_locator

		print("✅ ServiceLocator imported")

		from shared.interfaces.events import EventBus, event_bus

		print("✅ EventBus imported")

		# Test module containers (without wiring)
		from modules.auth.container import AuthContainer

		print("✅ AuthContainer imported")

		from modules.user.container import UserContainer

		print("✅ UserContainer imported")

		from modules.rbac.container import RBACContainer

		print("✅ RBACContainer imported")

		return True

	except Exception as e:
		print(f"❌ Import failed: {e}")
		return False


def test_module_creation():
	"""Probar creación de módulos"""
	print("\n🧪 Testing module creation...")

	try:
		# Test module interfaces
		from modules.auth.module import AuthModule

		auth_module = AuthModule()
		print(f"✅ AuthModule created: {auth_module.name}")

		from modules.user.module import UserModule

		user_module = UserModule()
		print(f"✅ UserModule created: {user_module.name}")

		return True

	except Exception as e:
		print(f"❌ Module creation failed: {e}")
		return False


def test_service_locator():
	"""Probar service locator"""
	print("\n🧪 Testing service locator...")

	try:
		from shared.interfaces.service_locator import service_locator

		# Test registration
		service_locator.register_service("test_service", "test_value")

		# Test retrieval
		value = service_locator.get_service("test_service")
		assert value == "test_value"

		print("✅ Service locator working")
		return True

	except Exception as e:
		print(f"❌ Service locator failed: {e}")
		return False


def main():
	"""Función principal"""
	print("🚀 Fast Hexagonal System Test")
	print("=" * 50)

	tests = [test_imports, test_module_creation, test_service_locator]

	passed = 0
	total = len(tests)

	for test in tests:
		if test():
			passed += 1

	print("\n" + "=" * 50)
	print(f"📊 Results: {passed}/{total} tests passed")

	if passed == total:
		print("🎉 All tests passed! System is working correctly.")
		return 0
	else:
		print("⚠️  Some tests failed. Check the output above.")
		return 1


if __name__ == "__main__":
	exit(main())
