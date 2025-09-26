#!/usr/bin/env python3
"""
Script de prueba para verificar que la inyección de dependencias funcione correctamente
"""

from core.fastapi.server.container_config import CoreContainer
from shared.dependencies import (
    get_user_service,
    get_auth_service,
    get_jwt_service,
    get_role_service,
    get_permission_service,
    get_currency_service,
    get_provider_service,
    get_draft_invoice_service,
    get_yiqi_service,
    get_app_module_service,
    get_user_relationship_service,
)

def test_container_initialization():
    """Prueba que el contenedor se inicialice correctamente"""
    try:
        container = CoreContainer()
        print("✅ CoreContainer inicializado correctamente")
        return container
    except Exception as e:
        print(f"❌ Error inicializando CoreContainer: {e}")
        return None

def test_dependency_functions():
    """Prueba que las funciones de dependencias funcionen"""
    container = test_container_initialization()
    if not container:
        return
    
    # Wire the container first
    container.wire(packages=["shared"])
    
    dependencies = [
        ("get_user_service", get_user_service),
        ("get_auth_service", get_auth_service),
        ("get_jwt_service", get_jwt_service),
        ("get_role_service", get_role_service),
        ("get_permission_service", get_permission_service),
        ("get_currency_service", get_currency_service),
        ("get_provider_service", get_provider_service),
        ("get_draft_invoice_service", get_draft_invoice_service),
        ("get_yiqi_service", get_yiqi_service),
        ("get_app_module_service", get_app_module_service),
        ("get_user_relationship_service", get_user_relationship_service),
    ]
    
    for name, func in dependencies:
        try:
            service = func()
            if service:
                print(f"✅ {name}: {type(service).__name__}")
            else:
                print(f"⚠️ {name}: Retornó None")
        except Exception as e:
            print(f"❌ {name}: Error - {e}")

if __name__ == "__main__":
    print("🧪 Probando sistema de inyección de dependencias...")
    print("=" * 50)
    test_dependency_functions()
    print("=" * 50)
    print("✅ Pruebas completadas")