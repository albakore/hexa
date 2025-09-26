"""
Auth Module - Service Registration (Fallback)
"""
from shared.interfaces.service_locator import service_locator


def register_services():
    """Registra los servicios del módulo Auth en Service Locator"""
    try:
        from modules.auth.container import AuthContainer
        container = AuthContainer()
        
        auth_service = container.auth_service_simple()
        jwt_service = container.jwt_service()
        
        service_locator.register_service("auth_service", auth_service)
        service_locator.register_service("jwt_service", jwt_service)
        
        print("✅ Auth services registered")
        
    except Exception as e:
        print(f"⚠️ Auth services registration failed: {e}")


# Auto-register when imported
if __name__ != "__main__":
    register_services()