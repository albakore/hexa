# Sistema de Desacoplamiento

## Arquitectura Desacoplada

El sistema implementa un desacoplamiento total entre módulos mediante interfaces y patrones de comunicación bien definidos.

## Componentes del Sistema

### 1. ModuleInterface
```python
class ModuleInterface(ABC):
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
```

### 2. ModuleRegistry
```python
class ModuleRegistry:
    def register(self, module: ModuleInterface) -> None:
        """Registra un módulo en el sistema"""
    
    def get_module(self, name: str) -> Optional[ModuleInterface]:
        """Obtiene un módulo por nombre"""
    
    def get_all_modules(self) -> Dict[str, ModuleInterface]:
        """Obtiene todos los módulos registrados"""
```

### 3. ServiceLocator
```python
class ServiceLocator:
    def register_service(self, name: str, service: Any) -> None:
        """Registra un servicio por nombre"""
    
    def get_service(self, name: str) -> Optional[Any]:
        """Obtiene un servicio por nombre"""
    
    def get_typed_service(self, name: str, service_type: Type[T]) -> Optional[T]:
        """Obtiene un servicio tipado"""
```

### 4. EventBus
```python
class EventBus:
    def subscribe(self, event_type: str, handler: EventHandler) -> None:
        """Suscribe un handler a un tipo de evento"""
    
    def publish(self, event: DomainEvent) -> None:
        """Publica un evento a todos los handlers suscritos"""
```

## Patrones de Comunicación

### 1. Service Locator Pattern
```python
# Módulo A registra su servicio
service_locator.register_service("user_service", user_service)

# Módulo B consume el servicio
user_service = service_locator.get_service("user_service")
if user_service:
    user = user_service.get_user(user_id)
```

### 2. Event-Driven Communication
```python
# Módulo publica evento
event = DomainEvent(
    event_type="user_created",
    data={"user_id": user.id, "email": user.email},
    timestamp=datetime.now(),
    module_source="user"
)
event_bus.publish(event)

# Otros módulos se suscriben
class NotificationHandler(EventHandler):
    def handle(self, event: DomainEvent) -> None:
        if event.event_type == "user_created":
            self.send_welcome_email(event.data["email"])

event_bus.subscribe("user_created", NotificationHandler())
```

## Ventajas del Desacoplamiento

### 1. **Independencia de Desarrollo**
- Equipos pueden trabajar en paralelo
- Ciclos de desarrollo independientes
- Testing aislado por módulo

### 2. **Escalabilidad**
- Módulos pueden ejecutarse en procesos separados
- Fácil migración a microservicios
- Escalado horizontal por módulo

### 3. **Mantenibilidad**
- Cambios localizados
- Menor riesgo de regresiones
- Refactoring seguro

### 4. **Flexibilidad**
- Intercambio de implementaciones
- Configuración dinámica
- A/B testing por módulo

## Implementación Práctica

### Registro de Módulo
```python
# modules/user/module.py
class UserModule(ModuleInterface):
    def __init__(self):
        self._container = UserContainer()
        self._routes = self._setup_routes()
    
    @property
    def name(self) -> str:
        return "user"
    
    @property
    def container(self) -> DeclarativeContainer:
        return self._container
    
    @property
    def routes(self) -> APIRouter:
        return self._routes
```

### Auto-registro
```python
# modules/__init__.py
def register_all_modules():
    from modules.user.module import UserModule
    from modules.auth.module import AuthModule
    
    module_registry.register(UserModule())
    module_registry.register(AuthModule())

register_all_modules()
```

### Configuración Principal
```python
# main.py
import modules  # Auto-registra módulos

# Configurar contenedores de módulos
module_containers = module_registry.get_containers()
for name, module_container in module_containers.items():
    module_container.wire(modules=[f"modules.{name}"])

# Agregar rutas
module_routes = module_registry.get_routes()
for route in module_routes:
    app.include_router(route)
```

## Reglas de Desacoplamiento

### ✅ Permitido
- Comunicación vía ServiceLocator
- Eventos asíncronos
- Interfaces compartidas en `shared/`
- Uso de DTOs para intercambio

### ❌ Prohibido
- Importación directa entre módulos
- Referencias a containers externos
- Dependencias circulares
- Estado compartido mutable

## Monitoreo del Desacoplamiento

### Health Check
```python
@app.get("/health")
async def health_check():
    registered_modules = list(module_registry.get_all_modules().keys())
    return {
        "status": "healthy",
        "modules": registered_modules,
        "architecture": "hexagonal_decoupled"
    }
```

### Métricas por Módulo
```python
# Cada módulo puede exponer sus métricas
@router.get("/metrics")
async def module_metrics():
    return {
        "module": "user",
        "active_connections": get_active_connections(),
        "requests_per_minute": get_rpm(),
        "health": "ok"
    }
```