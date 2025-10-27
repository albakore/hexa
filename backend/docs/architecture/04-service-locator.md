# Service Locator Pattern

## ¿Qué es Service Locator?

El **Service Locator** es un patrón que permite a los módulos comunicarse entre sí sin importaciones directas, manteniendo el desacoplamiento.

## Problema que Resuelve

Sin Service Locator:
```python
# ❌ Acoplamiento directo
from modules.user.application.service.user import UserService

def get_invoice_with_user(invoice_id):
    user_service = UserService()  # ❌ Importación directa
    # ...
```

**Problemas**:
- Acoplamiento fuerte entre módulos
- Dependencias circulares
- Difícil de testear
- Difícil cambiar implementaciones

Con Service Locator:
```python
# ✅ Desacoplado
from shared.interfaces.service_locator import service_locator

def get_invoice_with_user(invoice_id):
    user_service = service_locator.get_service("user_service")  # ✅ Desacoplado
    # ...
```

## Implementación

### Clase ServiceLocator

Ubicación: `shared/interfaces/service_locator.py`

```python
class ServiceLocator:
    def __init__(self):
        self._services: Dict[str, Any] = {}
        self._factories: Dict[str, Callable[[], Any]] = {}
        self._type_hints: Dict[str, Type] = {}
```

**Instancia global**:
```python
service_locator = ServiceLocator()  # Singleton global
```

## Métodos Principales

### 1. `register_service(name, service, type_hint=None)`

Registra un servicio en el locator.

```python
service_locator.register_service("user_service", user_service_instance)

# Con type hint (para mejor IDE support)
service_locator.register_service(
    "user_service", 
    user_service_instance,
    type_hint=UserServiceProtocol
)
```

**Cuándo se usa**: Automáticamente por `module.py` al registrar módulos.

### 2. `get_service(name) -> Any`

Obtiene un servicio por nombre.

```python
user_service = service_locator.get_service("user_service")

# Usar el servicio
user = await user_service.get_user_by_id(123)
```

**Retorna**: 
- El servicio si existe
- `None` si no existe

### 3. `get_typed_service(name, service_type) -> Optional[T]`

Obtiene un servicio con type hints para mejor soporte de IDE.

```python
from shared.interfaces.service_protocols import UserServiceProtocol

user_service = service_locator.get_typed_service(
    "user_service", 
    UserServiceProtocol
)

# Ahora el IDE conoce los métodos de UserServiceProtocol
user = await user_service.get_user_by_id(123)  # ✅ Autocomplete
```

### 4. `get_dependency(name) -> Callable`

Retorna una función para usar con FastAPI `Depends()`.

```python
from fastapi import APIRouter, Depends

router = APIRouter()

@router.get("/invoice/{id}")
async def get_invoice(
    id: int,
    user_service = Depends(service_locator.get_dependency("user_service"))
):
    user = await user_service.get_user_by_id(id)
    return user
```

### 5. `get_typed_dependency(name, service_type) -> Callable[[], T]`

Como `get_dependency` pero con type hints.

```python
@router.get("/invoice/{id}")
async def get_invoice(
    id: int,
    user_service: UserServiceProtocol = Depends(
        service_locator.get_typed_dependency("user_service", UserServiceProtocol)
    )
):
    # IDE conoce el tipo
    user = await user_service.get_user_by_id(id)
    return user
```

### 6. `clear()`

Limpia todos los servicios registrados. Útil para hot-reload y tests.

```python
service_locator.clear()
```

## Flujo de Registro

### 1. Módulo Define Servicios

```python
# modules/user/module.py
class UserModule(ModuleInterface):
    @property
    def service(self) -> Dict[str, object]:
        return {
            "user_service": self._container.user_service,
        }
```

### 2. Module Discovery Registra

```python
# shared/interfaces/module_discovery.py
def registre_module(subclass_attribute: type[ModuleInterface]):
    subclass_module = subclass_attribute()
    ModuleRegistry().register(subclass_module)
    
    # Registrar servicios en service_locator
    for name, service in subclass_module.service.items():
        service_locator.register_service(name, service)
```

### 3. Otros Módulos Usan

```python
# modules/invoicing/domain/usecase/invoice.py
from shared.interfaces.service_locator import service_locator

class GetInvoiceWithUser:
    async def execute(self, invoice_id: int):
        # Obtener servicio de otro módulo
        user_service = service_locator.get_service("user_service")
        
        invoice = await self.invoice_repo.get_by_id(invoice_id)
        user = await user_service.get_user_by_id(invoice.user_id)
        
        return {"invoice": invoice, "user": user}
```

## Servicios Registrados

Ver todos los servicios disponibles:

```python
# En un shell o endpoint
from shared.interfaces.service_locator import service_locator

# Ver nombres de servicios
print(list(service_locator._services.keys()))

# Resultado:
# [
#   'auth_service',
#   'auth.jwt_service',
#   'user_service',
#   'purchase_invoice_service',
#   'provider_service',
#   'rbac.role_service',
#   'rbac.permission_service',
#   # ...
# ]
```

## Convenciones de Nombres

### Servicios
```python
"{module}_service"  # Servicio principal
"purchase_invoice_service"
"user_service"
"provider_service"
```

### Servicios Adicionales
```python
"{module}.{service}_service"  # Servicios específicos
"auth.jwt_service"
"rbac.role_service"
"rbac.permission_service"
```

### Tasks
```python
"{module}_tasks"  # Diccionario de tasks
"invoicing_tasks"
"notifications_tasks"
```

## Type Safety con Protocols

Para mejor soporte de IDE, definir Protocols:

```python
# shared/interfaces/service_protocols.py
from typing import Protocol

class UserServiceProtocol(Protocol):
    """Protocol para el servicio de usuarios"""
    
    async def get_user_by_id(self, user_id: int) -> User:
        ...
    
    async def create_user(self, data: dict) -> User:
        ...
```

**Usar en código**:
```python
user_service = service_locator.get_typed_service(
    "user_service",
    UserServiceProtocol
)

# IDE ahora conoce todos los métodos
user = await user_service.get_user_by_id(123)  # ✅ Autocomplete
```

## Uso en Tests

### Mock de Servicios

```python
@pytest.fixture
def mock_user_service():
    mock = AsyncMock()
    mock.get_user_by_id.return_value = User(id=1, name="Test")
    return mock

@pytest.fixture
def setup_service_locator(mock_user_service):
    from shared.interfaces.service_locator import service_locator
    
    # Limpiar
    service_locator.clear()
    
    # Registrar mock
    service_locator.register_service("user_service", mock_user_service)
    
    yield
    
    # Limpiar al final
    service_locator.clear()

async def test_invoice_with_user(setup_service_locator):
    # El use case usará el mock
    usecase = GetInvoiceWithUser()
    result = await usecase.execute(123)
    
    assert result["user"].name == "Test"
```

## Ventajas

1. **Desacoplamiento**: Módulos no se importan directamente
2. **Testabilidad**: Fácil reemplazar servicios con mocks
3. **Flexibilidad**: Cambiar implementaciones sin modificar código
4. **Descubrimiento**: Servicios se registran automáticamente
5. **Type Safety**: Soporte con Protocols

## Desventajas y Mitigaciones

### Desventaja 1: Pérdida de Type Safety

**Mitigación**: Usar `get_typed_service()` con Protocols

```python
# ❌ Sin tipos
user_service = service_locator.get_service("user_service")

# ✅ Con tipos
user_service = service_locator.get_typed_service("user_service", UserServiceProtocol)
```

### Desventaja 2: Errores en Runtime

Si un servicio no existe, solo se descubre en runtime.

**Mitigación**: Tests de integración

```python
def test_all_services_registered():
    """Verifica que todos los servicios esperados estén registrados"""
    required_services = [
        "user_service",
        "purchase_invoice_service",
        "provider_service",
    ]
    
    for service_name in required_services:
        service = service_locator.get_service(service_name)
        assert service is not None, f"Service {service_name} not registered"
```

### Desventaja 3: Nombres como Strings

**Mitigación**: Constantes

```python
# shared/interfaces/service_names.py
class ServiceNames:
    USER_SERVICE = "user_service"
    INVOICE_SERVICE = "purchase_invoice_service"
    
# Uso
from shared.interfaces.service_names import ServiceNames

user_service = service_locator.get_service(ServiceNames.USER_SERVICE)
```

## Comparación con Alternatives

### vs. Dependency Injection Directa

**DI Directa**:
```python
class InvoiceService:
    def __init__(self, user_service: UserService):  # Acoplado a clase concreta
        self.user_service = user_service
```

**Service Locator**:
```python
class InvoiceService:
    def __init__(self):
        pass
    
    async def method(self):
        user_service = service_locator.get_service("user_service")  # Desacoplado
```

### vs. Event Bus

Service Locator es **síncrono** y **request-response**.  
Event Bus es **asíncrono** y **fire-and-forget**.

**Cuándo usar cada uno**:
- **Service Locator**: Necesitas respuesta inmediata (ej: obtener usuario)
- **Event Bus**: Notificaciones, no necesitas respuesta (ej: enviar email)

## Debugging

### Ver servicios registrados

```python
# En un endpoint de debug
@router.get("/debug/services")
def list_services():
    return {
        "services": list(service_locator._services.keys()),
        "count": len(service_locator._services)
    }
```

### Verificar servicio existe

```python
if not service_locator.get_service("user_service"):
    raise ValueError("user_service not registered")
```

## Próximos Pasos

- [Module Registry](./03-modules.md) - Cómo se registran los módulos
- [Dependency Injection](./05-dependency-injection.md) - Containers y DI
- [Crear un Módulo](../modules/02-creating-module.md) - Registrar tus servicios
