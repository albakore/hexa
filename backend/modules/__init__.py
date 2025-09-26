"""
Sistema de módulos desacoplados
"""

from shared.interfaces.module_registry import module_registry


# Importar y registrar todos los módulos automáticamente
def register_all_modules():
	"""Registra todos los módulos disponibles"""
	try:
		# Import all module implementations with correct class names
		from modules.auth.module import AuthModule
		from modules.user.module import UserModule
		from modules.rbac.module import RBACModule  # Correct class name
		from modules.finance.module import FinanceModule
		from modules.provider.module import ProviderModule
		from modules.user_relationships.module import UserRelationshipModule
		from modules.yiqi_erp.module import YiqiErpModule
		from modules.app_module.module import AppModuleModule
		
		# Register all modules
		modules = [
			AuthModule(),
			UserModule(),
			RBACModule(),
			FinanceModule(),
			ProviderModule(),
			UserRelationshipModule(),
			YiqiErpModule(),
			AppModuleModule()
		]
		
		for module in modules:
			module_registry.register(module)
			
		print(f"✅ Registered {len(modules)} modules successfully")
	except Exception as e:
		print(f"⚠️ Module registration failed: {e}")
		# Fallback: register simple routers directly
		from shared.interfaces.module_registry import ModuleInterface
		from modules.finance.adapter.input.api.v1.currency import currency_router
		from modules.auth.adapter.input.api.v1.auth import auth_router
		from modules.user.adapter.input.api.v1.user import user_router
		from modules.rbac.adapter.input.api.v1.rbac import rbac_router
		from modules.provider.adapter.input.api.v1.provider import provider_router
		from modules.provider.adapter.input.api.v1.draft_invoice import draft_invoice_router
		from modules.user_relationships.adapter.input.api.v1.user_relationship import user_relationship_router
		from modules.yiqi_erp.adapter.input.api.v1.yiqi_erp import yiqi_erp_router
		from modules.app_module.adapter.input.api.v1.module import module_router
		
		# Create simple module wrapper
		class SimpleModule(ModuleInterface):
			def __init__(self, name: str, router):
				self._name = name
				self._router = router
			
			@property
			def name(self) -> str:
				return self._name
				
			@property
			def container(self):
				return None
				
			@property
			def routes(self):
				return self._router
		
		# Register simple modules
		simple_modules = [
			SimpleModule("finance", currency_router),
			SimpleModule("auth", auth_router),
			SimpleModule("user", user_router),
			SimpleModule("rbac", rbac_router),
			SimpleModule("provider", provider_router),
			SimpleModule("draft_invoice", draft_invoice_router),
			SimpleModule("user_relationships", user_relationship_router),
			SimpleModule("yiqi_erp", yiqi_erp_router),
			SimpleModule("app_module", module_router)
		]
		
		for module in simple_modules:
			module_registry.register(module)
			
		print(f"✅ Registered {len(simple_modules)} modules via fallback")


# Auto-registrar módulos al importar
register_all_modules()

# Auto-registro simplificado con dependency-injector
from shared.interfaces.service_registry import auto_register_module_services
auto_register_module_services()

# Fallback registration for services with complex dependencies
try:
    import modules.auth.register_services
except:
    pass
