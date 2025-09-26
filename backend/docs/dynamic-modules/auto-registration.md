# Registro Automático de Módulos

## Sistema de Auto-registro

El sistema implementa un mecanismo de registro automático que permite que los módulos se registren dinámicamente sin necesidad de configuración manual en el código principal.

## Arquitectura del Auto-registro

### Componentes Principales

1. **ModuleInterface**: Interface común para todos los módulos
2. **ModuleRegistry**: Registro centralizado de módulos
3. **Auto-discovery**: Sistema de descubrimiento automático
4. **Module Loader**: Cargador dinámico de módulos

## Implementación del Auto-registro

### ModuleInterface
```python
# shared/interfaces/module_registry.py
from abc import ABC, abstractmethod
from typing import Optional, Any
from dependency_injector.containers import DeclarativeContainer

class ModuleInterface(ABC):
    """Interface que deben implementar todos los módulos"""
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Nombre único del módulo"""
        pass
    
    @property
    @abstractmethod
    def container(self) -> DeclarativeContainer:
        """Container de dependencias del módulo"""
        pass
    
    @property
    @abstractmethod
    def routes(self) -> Optional[Any]:
        """Rutas del módulo (APIRouter)"""
        pass
    
    @property
    def version(self) -> str:
        """Versión del módulo"""
        return "1.0.0"
    
    @property
    def dependencies(self) -> list[str]:
        """Lista de dependencias del módulo"""
        return []
    
    @property
    def enabled(self) -> bool:
        """Si el módulo está habilitado"""
        return True
    
    def initialize(self) -> None:
        """Inicialización del módulo"""
        pass
    
    def shutdown(self) -> None:
        """Limpieza del módulo"""
        pass
```

### ModuleRegistry
```python
# shared/interfaces/module_registry.py
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)

class ModuleRegistry:
    """Registro centralizado de módulos desacoplados"""
    
    def __init__(self):
        self._modules: Dict[str, ModuleInterface] = {}
        self._initialization_order: List[str] = []
        self._initialized: bool = False
    
    def register(self, module: ModuleInterface) -> None:
        """Registra un módulo en el sistema"""
        if module.name in self._modules:
            logger.warning(f"Module {module.name} already registered, skipping")
            return
        
        if not module.enabled:
            logger.info(f"Module {module.name} is disabled, skipping")
            return
        
        # Verificar dependencias
        if not self._check_dependencies(module):
            logger.error(f"Module {module.name} has unmet dependencies")
            return
        
        self._modules[module.name] = module
        logger.info(f"✅ Module registered: {module.name} v{module.version}")
        
        # Inicializar si el sistema ya está inicializado
        if self._initialized:
            self._initialize_module(module)
    
    def _check_dependencies(self, module: ModuleInterface) -> bool:
        """Verificar que las dependencias del módulo estén disponibles"""
        for dependency in module.dependencies:
            if dependency not in self._modules:
                logger.error(f"Dependency {dependency} not found for module {module.name}")
                return False
        return True
    
    def get_module(self, name: str) -> Optional[ModuleInterface]:
        """Obtiene un módulo por nombre"""
        return self._modules.get(name)
    
    def get_all_modules(self) -> Dict[str, ModuleInterface]:
        """Obtiene todos los módulos registrados"""
        return self._modules.copy()
    
    def get_containers(self) -> Dict[str, DeclarativeContainer]:
        """Obtiene todos los containers de los módulos"""
        return {name: module.container for name, module in self._modules.items()}
    
    def get_routes(self) -> list:
        """Obtiene todas las rutas de los módulos"""
        routes = []
        for module in self._modules.values():
            if module.routes:
                routes.append(module.routes)
        return routes
    
    def initialize_all(self) -> None:
        """Inicializar todos los módulos en orden de dependencias"""
        if self._initialized:
            return
        
        logger.info("🚀 Initializing all modules...")
        
        # Ordenar módulos por dependencias
        ordered_modules = self._resolve_dependency_order()
        
        # Inicializar en orden
        for module_name in ordered_modules:
            module = self._modules[module_name]
            self._initialize_module(module)
            self._initialization_order.append(module_name)
        
        self._initialized = True
        logger.info(f"✅ All modules initialized: {', '.join(ordered_modules)}")
    
    def _resolve_dependency_order(self) -> List[str]:
        """Resolver orden de inicialización basado en dependencias"""
        ordered = []
        visited = set()
        temp_visited = set()
        
        def visit(module_name: str):
            if module_name in temp_visited:
                raise ValueError(f"Circular dependency detected involving {module_name}")
            if module_name in visited:
                return
            
            temp_visited.add(module_name)
            
            module = self._modules[module_name]
            for dependency in module.dependencies:
                if dependency in self._modules:
                    visit(dependency)
            
            temp_visited.remove(module_name)
            visited.add(module_name)
            ordered.append(module_name)
        
        for module_name in self._modules:
            if module_name not in visited:
                visit(module_name)
        
        return ordered
    
    def _initialize_module(self, module: ModuleInterface) -> None:
        """Inicializar un módulo específico"""
        try:
            module.initialize()
            logger.info(f"✅ Module initialized: {module.name}")
        except Exception as e:
            logger.error(f"❌ Failed to initialize module {module.name}: {e}")
            raise
    
    def shutdown_all(self) -> None:
        """Cerrar todos los módulos en orden inverso"""
        if not self._initialized:
            return
        
        logger.info("🛑 Shutting down all modules...")
        
        # Cerrar en orden inverso
        for module_name in reversed(self._initialization_order):
            module = self._modules[module_name]
            try:
                module.shutdown()
                logger.info(f"✅ Module shutdown: {module_name}")
            except Exception as e:
                logger.error(f"❌ Error shutting down module {module_name}: {e}")
        
        self._initialized = False
        self._initialization_order.clear()

# Instancia global del registro
module_registry = ModuleRegistry()
```

## Auto-discovery de Módulos

### Module Discoverer
```python
# shared/interfaces/module_discoverer.py
import os
import importlib
import inspect
from pathlib import Path
from typing import List, Type
import logging

logger = logging.getLogger(__name__)

class ModuleDiscoverer:
    """Descubridor automático de módulos"""
    
    def __init__(self, modules_path: str = "modules"):
        self.modules_path = modules_path
    
    def discover_modules(self) -> List[ModuleInterface]:
        """Descubrir todos los módulos disponibles"""
        modules = []
        modules_dir = Path(self.modules_path)
        
        if not modules_dir.exists():
            logger.warning(f"Modules directory {self.modules_path} not found")
            return modules
        
        # Buscar en cada subdirectorio
        for module_dir in modules_dir.iterdir():
            if module_dir.is_dir() and not module_dir.name.startswith('_'):
                module_instance = self._load_module(module_dir.name)
                if module_instance:
                    modules.append(module_instance)
        
        return modules
    
    def _load_module(self, module_name: str) -> Optional[ModuleInterface]:
        """Cargar un módulo específico"""
        try:
            # Intentar importar el archivo module.py
            module_path = f"{self.modules_path}.{module_name}.module"
            module_module = importlib.import_module(module_path)
            
            # Buscar clases que implementen ModuleInterface
            for name, obj in inspect.getmembers(module_module):
                if (inspect.isclass(obj) and 
                    issubclass(obj, ModuleInterface) and 
                    obj != ModuleInterface):
                    
                    # Instanciar el módulo
                    module_instance = obj()
                    logger.info(f"📦 Discovered module: {module_instance.name}")
                    return module_instance
            
            logger.warning(f"No ModuleInterface implementation found in {module_name}")
            return None
            
        except ImportError as e:
            logger.warning(f"Could not import module {module_name}: {e}")
            return None
        except Exception as e:
            logger.error(f"Error loading module {module_name}: {e}")
            return None
    
    def auto_register_modules(self, registry: ModuleRegistry) -> None:
        """Descubrir y registrar automáticamente todos los módulos"""
        logger.info("🔍 Auto-discovering modules...")
        
        modules = self.discover_modules()
        
        for module in modules:
            registry.register(module)
        
        logger.info(f"📦 Auto-discovery complete. Found {len(modules)} modules")

# Instancia global del descubridor
module_discoverer = ModuleDiscoverer()
```

## Implementación en Módulos

### Ejemplo de Módulo con Auto-registro
```python
# modules/user/module.py
from fastapi import APIRouter
from dependency_injector.containers import DeclarativeContainer

from shared.interfaces.module_registry import ModuleInterface
from modules.user.container import UserContainer
from core.fastapi.server.route_helpers import get_routes, set_routes_to_app

class UserModule(ModuleInterface):
    """Módulo de usuarios con auto-registro"""
    
    def __init__(self):
        self._container = None
        self._routes = None
        self._initialized = False
    
    @property
    def name(self) -> str:
        return "user"
    
    @property
    def version(self) -> str:
        return "1.2.0"
    
    @property
    def dependencies(self) -> list[str]:
        return ["auth"]  # Depende del módulo de autenticación
    
    @property
    def enabled(self) -> bool:
        # Puede ser controlado por configuración
        return os.getenv("USER_MODULE_ENABLED", "true").lower() == "true"
    
    @property
    def container(self) -> DeclarativeContainer:
        if not self._container:
            self._container = UserContainer()
        return self._container
    
    @property
    def routes(self) -> APIRouter:
        if not self._routes:
            self._routes = self._setup_routes()
        return self._routes
    
    def initialize(self) -> None:
        """Inicialización del módulo"""
        if self._initialized:
            return
        
        logger.info(f"Initializing {self.name} module...")
        
        # Configurar container
        self.container.wire(modules=[f"modules.{self.name}"])
        
        # Registrar servicios en el service locator
        from shared.interfaces.service_locator import service_locator
        service_locator.register_service("user_service", self.container.service())
        
        # Suscribirse a eventos
        from shared.interfaces.events import event_bus
        event_bus.subscribe("auth_user_created", self._handle_user_created)
        
        self._initialized = True
        logger.info(f"✅ {self.name} module initialized")
    
    def shutdown(self) -> None:
        """Limpieza del módulo"""
        if not self._initialized:
            return
        
        logger.info(f"Shutting down {self.name} module...")
        
        # Limpiar recursos
        if hasattr(self.container, 'shutdown'):
            self.container.shutdown()
        
        self._initialized = False
        logger.info(f"✅ {self.name} module shutdown")
    
    def _setup_routes(self) -> APIRouter:
        """Configurar rutas del módulo"""
        routes = get_routes(f"modules.{self.name}")
        router = APIRouter(prefix="/users", tags=["Users"])
        set_routes_to_app(router, routes)
        return router
    
    def _handle_user_created(self, event):
        """Manejar evento de usuario creado"""
        logger.info(f"User module handling user_created event: {event.data}")
        # Lógica específica del módulo
```

## Sistema de Configuración de Módulos

### Module Configuration
```python
# shared/interfaces/module_config.py
from dataclasses import dataclass
from typing import Dict, Any, Optional
import os
import json
import yaml

@dataclass
class ModuleConfig:
    """Configuración de un módulo"""
    name: str
    enabled: bool = True
    version: str = "1.0.0"
    dependencies: list[str] = None
    settings: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []
        if self.settings is None:
            self.settings = {}

class ModuleConfigLoader:
    """Cargador de configuración de módulos"""
    
    def __init__(self, config_path: str = "config/modules.yaml"):
        self.config_path = config_path
    
    def load_config(self) -> Dict[str, ModuleConfig]:
        """Cargar configuración de módulos"""
        if not os.path.exists(self.config_path):
            return {}
        
        try:
            with open(self.config_path, 'r') as f:
                if self.config_path.endswith('.yaml') or self.config_path.endswith('.yml'):
                    data = yaml.safe_load(f)
                else:
                    data = json.load(f)
            
            configs = {}
            for module_name, config_data in data.get('modules', {}).items():
                configs[module_name] = ModuleConfig(
                    name=module_name,
                    enabled=config_data.get('enabled', True),
                    version=config_data.get('version', '1.0.0'),
                    dependencies=config_data.get('dependencies', []),
                    settings=config_data.get('settings', {})
                )
            
            return configs
            
        except Exception as e:
            logger.error(f"Error loading module config: {e}")
            return {}
    
    def save_config(self, configs: Dict[str, ModuleConfig]) -> None:
        """Guardar configuración de módulos"""
        data = {
            'modules': {
                name: {
                    'enabled': config.enabled,
                    'version': config.version,
                    'dependencies': config.dependencies,
                    'settings': config.settings
                }
                for name, config in configs.items()
            }
        }
        
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        
        with open(self.config_path, 'w') as f:
            if self.config_path.endswith('.yaml') or self.config_path.endswith('.yml'):
                yaml.dump(data, f, default_flow_style=False)
            else:
                json.dump(data, f, indent=2)
```

### Ejemplo de Configuración
```yaml
# config/modules.yaml
modules:
  user:
    enabled: true
    version: "1.2.0"
    dependencies: ["auth"]
    settings:
      max_users_per_page: 50
      enable_user_registration: true
  
  finance:
    enabled: true
    version: "1.0.0"
    dependencies: ["user"]
    settings:
      default_currency: "USD"
      enable_multi_currency: true
  
  yiqi_erp:
    enabled: false  # Módulo deshabilitado
    version: "1.1.0"
    dependencies: ["finance", "provider"]
    settings:
      api_timeout: 30
      retry_attempts: 3
```

## Inicialización Automática

### Auto-registration System
```python
# modules/__init__.py
"""
Sistema de auto-registro de módulos
"""
import logging
from shared.interfaces.module_registry import module_registry
from shared.interfaces.module_discoverer import module_discoverer
from shared.interfaces.module_config import ModuleConfigLoader

logger = logging.getLogger(__name__)

def auto_register_modules():
    """Registrar automáticamente todos los módulos disponibles"""
    logger.info("🚀 Starting automatic module registration...")
    
    # Cargar configuración de módulos
    config_loader = ModuleConfigLoader()
    module_configs = config_loader.load_config()
    
    # Descubrir y registrar módulos
    module_discoverer.auto_register_modules(module_registry)
    
    # Aplicar configuración
    for module_name, config in module_configs.items():
        module = module_registry.get_module(module_name)
        if module:
            # Aplicar configuración específica del módulo
            if hasattr(module, 'apply_config'):
                module.apply_config(config)
    
    # Inicializar todos los módulos
    module_registry.initialize_all()
    
    logger.info("✅ Automatic module registration completed")

# Auto-registrar módulos al importar
auto_register_modules()
```

## Integración con FastAPI

### Application Factory con Auto-registro
```python
# main.py
"""
Punto de entrada principal con auto-registro de módulos
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

# Importar módulos para auto-registro (debe ser lo primero)
import modules

from core.fastapi.server.container_config import CoreContainer
from shared.interfaces.module_registry import module_registry
from core.fastapi.middlewares.authentication import AuthenticationMiddleware
from core.fastapi.middlewares.sqlalchemy import SQLAlchemyMiddleware
from core.fastapi.middlewares.response_log import ResponseLogMiddleware

logger = logging.getLogger(__name__)

def create_app() -> FastAPI:
    """Crear y configurar la aplicación FastAPI con módulos auto-registrados"""
    
    logger.info("🚀 Creating FastAPI application...")
    
    # Crear aplicación
    app = FastAPI(
        title="Fast Hexagonal API",
        description="API con arquitectura hexagonal y módulos auto-registrados",
        version="2.0.0"
    )
    
    # Configurar CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Agregar middlewares
    app.add_middleware(ResponseLogMiddleware)
    app.add_middleware(AuthenticationMiddleware)
    app.add_middleware(SQLAlchemyMiddleware)
    
    # Configurar contenedor principal
    container = CoreContainer()
    app.container = container
    
    # Configurar contenedores de módulos auto-registrados
    module_containers = module_registry.get_containers()
    for name, module_container in module_containers.items():
        try:
            module_container.wire(modules=[f"modules.{name}"])
            logger.info(f"✅ Wired container for module: {name}")
        except Exception as e:
            logger.error(f"❌ Failed to wire container for module {name}: {e}")
    
    # Agregar rutas de módulos auto-registrados
    module_routes = module_registry.get_routes()
    for route in module_routes:
        app.include_router(route)
        logger.info(f"✅ Included routes for module")
    
    # Agregar eventos de ciclo de vida
    @app.on_event("startup")
    async def startup_event():
        logger.info("🚀 Application startup")
        # Los módulos ya están inicializados por el auto-registro
    
    @app.on_event("shutdown")
    async def shutdown_event():
        logger.info("🛑 Application shutdown")
        module_registry.shutdown_all()
    
    logger.info(f"✅ FastAPI application created with {len(module_containers)} modules")
    return app

# Crear aplicación
app = create_app()

@app.get("/health")
async def health_check():
    """Endpoint de verificación de salud con información de módulos"""
    registered_modules = module_registry.get_all_modules()
    
    module_info = {}
    for name, module in registered_modules.items():
        module_info[name] = {
            "version": module.version,
            "dependencies": module.dependencies,
            "enabled": module.enabled
        }
    
    return {
        "status": "healthy",
        "modules": module_info,
        "total_modules": len(registered_modules),
        "architecture": "hexagonal_decoupled_auto_registered"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

## Beneficios del Auto-registro

### 1. **Simplicidad de Desarrollo**
- No necesidad de modificar código central para nuevos módulos
- Registro automático al agregar módulos
- Configuración declarativa

### 2. **Flexibilidad**
- Módulos pueden ser habilitados/deshabilitados dinámicamente
- Configuración externa de módulos
- Carga condicional basada en entorno

### 3. **Mantenibilidad**
- Menos acoplamiento entre módulos y aplicación principal
- Fácil adición/remoción de módulos
- Gestión centralizada de dependencias

### 4. **Escalabilidad**
- Soporte para gran número de módulos
- Inicialización optimizada por dependencias
- Gestión eficiente de recursos

El sistema de auto-registro proporciona una base sólida para el crecimiento y evolución de la aplicación, manteniendo la flexibilidad y simplicidad en el desarrollo de nuevos módulos.