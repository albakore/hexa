"""
Sistema simplificado de auto-registro
"""
from pathlib import Path
import importlib.util


def auto_register_module_services():
    """Auto-registra servicios usando dependency-injector containers"""
    print("🎯 Using dependency-injector containers - no manual registration needed")
    
    # Los containers se resuelven automáticamente via dependency-injector
    # Solo verificamos que los módulos existan
    modules_path = Path("modules")
    module_count = 0
    
    for module_dir in modules_path.iterdir():
        if module_dir.is_dir() and not module_dir.name.startswith('_'):
            container_file = module_dir / "container.py"
            if container_file.exists():
                module_count += 1
                print(f"✅ {module_dir.name} container available")
    
    print(f"📦 Found {module_count} module containers")