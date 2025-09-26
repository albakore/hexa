# Arquitectura Hexagonal Desacoplada

## Descripción General

El proyecto ha sido refactorizado para implementar una arquitectura hexagonal completamente desacoplada, donde cada módulo es independiente y se comunica a través de interfaces bien definidas.

## Estructura de Módulos

### Ubicación
Todos los módulos se encuentran en la carpeta `modules/`:

```
modules/
├── auth/                 # Autenticación y autorización
├── user/                 # Gestión de usuarios
├── rbac/                 # Control de acceso basado en roles
├── user_relationships/   # Relaciones entre usuarios
├── app_module/          # Módulos de aplicación
├── finance/             # Módulo financiero
├── provider/            # Gestión de proveedores
├── yiqi_erp/           # Integración con YiQi ERP
└── __init__.py         # Auto-registro de módulos
```

### Estructura de Cada Módulo

Cada módulo sigue la arquitectura hexagonal:

```
module_name/
├── adapter/
│   ├── input/
│   │   └── api/         # Controladores REST
│   └── output/
│       └── persistence/ # Repositorios y adaptadores
├── application/
│   ├── dto/            # Data Transfer Objects
│   ├── service/        # Servicios de aplicación
│   └── exception/      # Excepciones específicas
├── domain/
│   ├── entity/         # Entidades de dominio
│   ├── repository/     # Interfaces de repositorio
│   ├── usecase/        # Casos de uso
│   └── vo/            # Value Objects
├── container.py        # Contenedor de dependencias
└── module.py          # Definición del módulo
```

## Sistema de Desacoplamiento

### 1. Registro de Módulos

Cada módulo implementa la interfaz `ModuleInterface`:

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

### 2. Auto-registro

Los módulos se registran automáticamente al importar `modules`:

```python
# modules/__init__.py
from shared.interfaces.module_registry import module_registry

def register_all_modules():
    from modules.auth.module import AuthModule
    from modules.user.module import UserModule
    # ... otros módulos
    
    module_registry.register(AuthModule())
    module_registry.register(UserModule())
    # ... registrar otros módulos
```

### 3. Comunicación Entre Módulos

#### Service Locator
Para acceder a servicios de otros módulos:

```python
from shared.interfaces.service_locator import service_locator

# Obtener servicio de otro módulo
user_service = service_locator.get_service("user_service")
```

#### Event Bus
Para comunicación asíncrona entre módulos:

```python
from shared.interfaces.events import event_bus, DomainEvent

# Publicar evento
event = DomainEvent(
    event_type="user_created",
    data={"user_id": user.id},
    timestamp=datetime.now(),
    module_source="user"
)
event_bus.publish(event)

# Suscribirse a eventos
event_bus.subscribe("user_created", MyEventHandler())
```

## Ventajas de la Nueva Arquitectura

### 1. **Desacoplamiento Total**
- Cada módulo es completamente independiente
- No hay dependencias directas entre módulos
- Fácil testing unitario de cada módulo

### 2. **Escalabilidad**
- Nuevos módulos se pueden agregar sin modificar código existente
- Módulos pueden ser desarrollados por equipos independientes
- Posibilidad de extraer módulos a microservicios

### 3. **Mantenibilidad**
- Cambios en un módulo no afectan otros
- Código más limpio y organizado
- Responsabilidades bien definidas

### 4. **Flexibilidad**
- Módulos pueden ser habilitados/deshabilitados dinámicamente
- Diferentes implementaciones para diferentes entornos
- Fácil intercambio de implementaciones

## Migración desde la Arquitectura Anterior

### Cambios Principales

1. **Movimiento de Módulos**: Todos los módulos de `app/` se movieron a `modules/`
2. **Eliminación de Dependencias Directas**: Los containers ya no referencian directamente otros containers
3. **Sistema de Registro**: Implementación del `ModuleRegistry` para gestión centralizada
4. **Interfaces de Comunicación**: `ServiceLocator` y `EventBus` para comunicación entre módulos

### Compatibilidad

La nueva arquitectura mantiene la funcionalidad existente mientras proporciona:
- Mejor separación de responsabilidades
- Mayor flexibilidad para futuras extensiones
- Base sólida para evolución a microservicios

## Uso

### Ejecutar la Aplicación

```bash
python main.py
```

### Verificar Módulos Registrados

```bash
curl http://localhost:8000/health
```

Respuesta:
```json
{
    "status": "healthy",
    "modules": ["auth", "user", "rbac", "finance", "provider", "yiqi_erp"],
    "architecture": "hexagonal_decoupled"
}
```

## Próximos Pasos

1. **Implementar Event Handlers**: Agregar manejadores de eventos específicos para cada módulo
2. **Service Discovery**: Mejorar el sistema de descubrimiento de servicios
3. **Health Checks**: Implementar verificaciones de salud por módulo
4. **Métricas**: Agregar métricas y monitoreo por módulo
5. **Documentación API**: Generar documentación automática por módulo