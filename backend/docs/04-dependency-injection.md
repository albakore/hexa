# Sistema de Dependencias

## Introducción

El proyecto utiliza **dependency_injector** para gestionar las dependencias de manera automática y desacoplada. Cada módulo tiene su propio contenedor de dependencias.

## Conceptos Clave

### 1. Container
Contenedor que define y gestiona las dependencias de un módulo.

### 2. Providers
Definen cómo crear las instancias de las dependencias:
- **Factory**: Crea nueva instancia cada vez
- **Singleton**: Una sola instancia compartida
- **Object**: Instancia existente

### 3. Wiring
Proceso de inyección automática en funciones decoradas con `@inject`

## Estructura de un Container

```python
# modules/[module]/container.py
from dependency_injector.providers import Factory, Singleton
from dependency_injector.containers import DeclarativeContainer

class UserContainer(DeclarativeContainer):
    # Singleton - Una sola instancia
    repository = Singleton(
        UserSQLAlchemyRepository,
    )
    
    # Factory - Nueva instancia cada vez
    repository_adapter = Factory(
        UserRepositoryAdapter, 
        repository=repository
    )
    
    # Servicio principal
    service = Factory(
        UserService, 
        repository=repository_adapter
    )
```

## Tipos de Providers

### Factory Provider
Crea una nueva instancia cada vez que se solicita.

```python
# Definición
service = Factory(UserService, repository=repository_adapter)

# Uso
user_service = container.service()  # Nueva instancia
another_service = container.service()  # Otra instancia nueva
```

### Singleton Provider
Crea una sola instancia que se reutiliza.

```python
# Definición
repository = Singleton(UserSQLAlchemyRepository)

# Uso
repo1 = container.repository()  # Primera instancia
repo2 = container.repository()  # Misma instancia que repo1
```

### Object Provider
Usa una instancia existente.

```python
from core.db.session import session

# Definición
db_session = Object(session)

# Uso
session_instance = container.db_session()  # Instancia existente
```

## Inyección en Rutas FastAPI

### Método 1: @inject + Provide (Recomendado para servicios internos)

```python
from dependency_injector.wiring import Provide, inject
from fastapi import Depends

@user_router.post("")
@inject
async def create_user(
    request: CreateUserRequest,
    user_service: UserService = Depends(Provide[UserContainer.service]),
):
    return await user_service.create_user(request)
```

### Método 2: Service Locator (Recomendado para servicios externos)

```python
from shared.interfaces.service_locator import service_locator

@user_router.get("/search")
async def search_users(
    role_service = Depends(service_locator.get_dependency("rbac.role_service")),
    user_service: UserService = Depends(Provide[UserContainer.service]),
):
    # Usar ambos servicios
    pass
```

## Configuración de Dependencias

### Dependencias Simples
```python
class UserContainer(DeclarativeContainer):
    service = Factory(UserService)
```

### Dependencias con Parámetros
```python
class UserContainer(DeclarativeContainer):
    service = Factory(
        UserService,
        repository=repository_adapter,
        cache_ttl=300
    )
```

### Dependencias Condicionales
```python
from core.config.settings import env

class UserContainer(DeclarativeContainer):
    repository = Factory(
        UserSQLAlchemyRepository if env.USE_SQL else UserMemoryRepository
    )
```

### Dependencias de Otros Módulos
```python
from modules.rbac.container import RBACContainer

class UserContainer(DeclarativeContainer):
    service = Factory(
        UserService,
        repository=repository_adapter,
        rbac_service=RBACContainer.service  # Dependencia externa
    )
```

## Wiring y Auto-discovery

### Wiring Manual
```python
# En module.py
class UserModule(ModuleInterface):
    def __init__(self):
        self._container = UserContainer()
        # Wiring manual específico
        self._container.wire(modules=["modules.user.adapter.input.api.v1.user"])
```

### Auto-discovery
El sistema automáticamente:
1. Descubre módulos en la carpeta `modules/`
2. Registra sus servicios en el service_locator
3. Configura las rutas en FastAPI

## Resolución de Dependencias

### Orden de Resolución
1. **Providers internos**: Definidos en el container del módulo
2. **Service Locator**: Para dependencias entre módulos
3. **FastAPI Depends**: Para dependencias de framework

### Ejemplo Complejo
```python
class OrderContainer(DeclarativeContainer):
    # Dependencias internas
    repository = Singleton(OrderRepository)
    
    # Dependencias externas (otros módulos)
    user_service = Object(service_locator.get_service("user_service"))
    payment_service = Object(service_locator.get_service("payment_service"))
    
    # Servicio principal
    service = Factory(
        OrderService,
        repository=repository,
        user_service=user_service,
        payment_service=payment_service
    )
```

## Testing con Dependency Injection

### Mock de Dependencias
```python
import pytest
from unittest.mock import AsyncMock
from modules.user.container import UserContainer

@pytest.fixture
def mock_container():
    container = UserContainer()
    
    # Override con mock
    mock_repository = AsyncMock()
    container.repository_adapter.override(mock_repository)
    
    return container

async def test_user_service(mock_container):
    service = mock_container.service()
    # Test con dependencias mockeadas
```

### Test de Integración
```python
@pytest.fixture
def test_container():
    container = UserContainer()
    
    # Override con implementación de test
    container.repository.override(InMemoryUserRepository())
    
    return container
```

## Buenas Prácticas

### ✅ Hacer
- Usar Factory para servicios stateless
- Usar Singleton para recursos compartidos (DB, cache)
- Definir interfaces claras entre módulos
- Usar service_locator para comunicación entre módulos

### ❌ Evitar
- Dependencias circulares entre módulos
- Singletons para servicios con estado mutable
- Acceso directo a containers de otros módulos
- Mezclar lógica de negocio en containers

## Debugging

### Ver Dependencias Registradas
```python
# En desarrollo
container = UserContainer()
print(container.providers)  # Lista todos los providers
```

### Verificar Wiring
```python
# Verificar si el wiring funcionó
print(container.wired_modules)
```

### Logs de Inyección
```python
import logging
logging.getLogger('dependency_injector').setLevel(logging.DEBUG)
```