# Inyección de Dependencias en Rutas

## Introducción

Este documento explica cómo inyectar servicios en las rutas de FastAPI, combinando **dependency_injector** para servicios internos y **service_locator** para servicios externos.

## Patrones de Inyección

### 1. Servicios Internos del Módulo

Para servicios que pertenecen al mismo módulo, usa `@inject` + `Provide`:

```python
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

@user_router.post("")
@inject
async def create_user(
    request: CreateUserRequest,
    user_service: UserService = Depends(Provide[UserContainer.service]),
):
    return await user_service.create_user(request)
```

**Características:**
- ✅ **Tipado fuerte**: IDE puede inferir tipos
- ✅ **Performance**: Resolución directa del container
- ✅ **Debugging**: Stack traces claros
- ❌ **Solo para servicios internos**: No funciona para otros módulos

### 2. Servicios Externos (Otros Módulos)

Para servicios de otros módulos, usa `service_locator.get_dependency()`:

```python
from shared.interfaces.service_locator import service_locator

@user_router.get("/search")
async def search_users(
    role_service = Depends(service_locator.get_dependency("rbac.role_service")),
    app_service = Depends(service_locator.get_dependency("app_module_service")),
):
    # Usar servicios externos
    roles = await role_service.get_all_roles()
    modules = await app_service.get_all_modules()
    return {"roles": roles, "modules": modules}
```

**Características:**
- ✅ **Desacoplamiento**: No depende directamente de otros módulos
- ✅ **Flexibilidad**: Fácil intercambiar implementaciones
- ✅ **Modularidad**: Los módulos siguen siendo independientes
- ❌ **Tipado débil**: IDE no puede inferir tipos automáticamente

### 3. Patrón Híbrido (Recomendado)

Combina ambos enfoques según el tipo de dependencia:

```python
@user_router.get("/{user_id}/permissions")
@inject
async def get_user_permissions(
    user_id: str,
    # Servicio interno - tipado fuerte
    user_service: UserService = Depends(Provide[UserContainer.service]),
    # Servicios externos - desacoplados
    role_service = Depends(service_locator.get_dependency("rbac.role_service")),
    permission_service = Depends(service_locator.get_dependency("rbac.permission_service")),
):
    user = await user_service.get_user_by_id(user_id)
    user_roles = await role_service.get_user_roles(user_id)
    permissions = await permission_service.get_permissions_by_roles(user_roles)
    
    return {
        "user": user,
        "roles": user_roles,
        "permissions": permissions
    }
```

## Configuración de Rutas

### Estructura Recomendada

```python
# modules/[module]/adapter/input/api/v1/[entity].py
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Query
from typing import List

from modules.[module].container import [Module]Container
from modules.[module].application.service.[entity] import [Entity]Service
from modules.[module].adapter.input.api.v1.request import Create[Entity]Request
from shared.interfaces.service_locator import service_locator

[entity]_router = APIRouter()

# Servicios internos con @inject
@[entity]_router.post("")
@inject
async def create_[entity](
    request: Create[Entity]Request,
    service: [Entity]Service = Depends(Provide[[Module]Container.service]),
) -> [Entity]Response:
    return await service.create_[entity](request)

# Servicios mixtos
@[entity]_router.get("/search")
@inject
async def search_[entity]s(
    query: str = Query(),
    # Interno
    service: [Entity]Service = Depends(Provide[[Module]Container.service]),
    # Externos
    auth_service = Depends(service_locator.get_dependency("auth_service")),
    rbac_service = Depends(service_locator.get_dependency("rbac.role_service")),
):
    # Verificar permisos
    user = await auth_service.get_current_user()
    has_permission = await rbac_service.check_permission(user.id, "search_[entity]s")
    
    if not has_permission:
        raise HTTPException(403, "Insufficient permissions")
    
    return await service.search_[entity]s(query)
```

## Manejo de Errores

### Servicios No Encontrados

```python
@router.get("/example")
async def example_endpoint(
    external_service = Depends(service_locator.get_dependency("non_existent_service")),
):
    if external_service is None:
        raise HTTPException(503, "External service not available")
    
    return await external_service.do_something()
```

### Validación de Dependencias

```python
from fastapi import HTTPException

def validate_service_dependency(service_name: str):
    def dependency():
        service = service_locator.get_service(service_name)
        if service is None:
            raise HTTPException(503, f"Service {service_name} not available")
        return service
    return dependency

@router.get("/example")
async def example_endpoint(
    rbac_service = Depends(validate_service_dependency("rbac.role_service")),
):
    return await rbac_service.get_all_roles()
```

## Tipado de Servicios Externos

### Usando Type Hints

```python
from typing import Any, cast
from modules.rbac.application.service.role import RoleService

@router.get("/users/{user_id}/roles")
async def get_user_roles(
    user_id: str,
    rbac_service: Any = Depends(service_locator.get_dependency("rbac.role_service")),
):
    # Cast para ayudar al IDE
    role_service = cast(RoleService, rbac_service)
    return await role_service.get_user_roles(user_id)
```

### Usando Protocols

```python
from typing import Protocol

class RoleServiceProtocol(Protocol):
    async def get_user_roles(self, user_id: str) -> List[str]: ...
    async def assign_role(self, user_id: str, role_id: int) -> bool: ...

@router.get("/users/{user_id}/roles")
async def get_user_roles(
    user_id: str,
    rbac_service: RoleServiceProtocol = Depends(service_locator.get_dependency("rbac.role_service")),
):
    # Ahora el IDE conoce los métodos disponibles
    return await rbac_service.get_user_roles(user_id)
```

## Middleware y Dependencias Globales

### Dependencias Globales

```python
# En el router principal
from core.fastapi.dependencies.auth import get_current_user

router = APIRouter(
    dependencies=[Depends(get_current_user)]  # Aplicado a todas las rutas
)
```

### Dependencias Condicionales

```python
from core.config.settings import env

def get_cache_service():
    if env.ENABLE_CACHE:
        return service_locator.get_service("cache_service")
    return None

@router.get("/cached-data")
async def get_cached_data(
    cache_service = Depends(get_cache_service),
):
    if cache_service:
        cached = await cache_service.get("data_key")
        if cached:
            return cached
    
    # Fallback sin cache
    return await generate_data()
```

## Testing de Rutas

### Mock de Dependencias Internas

```python
import pytest
from unittest.mock import AsyncMock
from fastapi.testclient import TestClient

def test_create_user_endpoint():
    # Mock del container
    mock_service = AsyncMock()
    mock_service.create_user.return_value = {"id": 1, "name": "Test"}
    
    # Override del provider
    with UserContainer.service.override(mock_service):
        response = client.post("/users", json={"name": "Test"})
        assert response.status_code == 200
```

### Mock de Dependencias Externas

```python
def test_search_users_endpoint():
    # Mock de servicios externos
    mock_rbac = AsyncMock()
    mock_rbac.get_user_roles.return_value = ["admin"]
    
    service_locator.register_service("rbac.role_service", mock_rbac)
    
    try:
        response = client.get("/users/search?query=test")
        assert response.status_code == 200
    finally:
        service_locator.clear()
```

## Buenas Prácticas

### ✅ Hacer

1. **Usar @inject para servicios internos**
   ```python
   @inject
   async def endpoint(service: MyService = Depends(Provide[Container.service])):
   ```

2. **Usar service_locator para servicios externos**
   ```python
   async def endpoint(external = Depends(service_locator.get_dependency("external_service"))):
   ```

3. **Validar servicios críticos**
   ```python
   if external_service is None:
       raise HTTPException(503, "Service unavailable")
   ```

4. **Documentar dependencias**
   ```python
   async def endpoint(
       # Internal service for user management
       user_service: UserService = Depends(Provide[UserContainer.service]),
       # External service for role validation
       rbac_service = Depends(service_locator.get_dependency("rbac.role_service")),
   ):
   ```

### ❌ Evitar

1. **Mezclar patrones sin razón**
   ```python
   # ❌ No hagas esto
   @inject
   async def endpoint(
       internal_service = Depends(service_locator.get_dependency("internal_service")),
   ):
   ```

2. **Dependencias circulares**
   ```python
   # ❌ Module A depende de Module B y viceversa
   ```

3. **Acceso directo a containers**
   ```python
   # ❌ No hagas esto
   async def endpoint():
       service = UserContainer().service()
   ```

4. **Ignorar errores de servicios faltantes**
   ```python
   # ❌ No hagas esto
   async def endpoint(service = Depends(service_locator.get_dependency("service"))):
       return await service.do_something()  # Puede fallar si service es None
   ```

## Debugging

### Verificar Inyección

```python
import logging

# Habilitar logs de dependency_injector
logging.getLogger('dependency_injector').setLevel(logging.DEBUG)

# Los logs mostrarán qué dependencias se están resolviendo
```

### Inspeccionar Dependencias en Runtime

```python
@router.get("/debug/dependencies")
async def debug_dependencies():
    return {
        "internal_services": list(UserContainer().providers.keys()),
        "external_services": list(service_locator._services.keys()),
        "factories": list(service_locator._factories.keys()),
    }
```