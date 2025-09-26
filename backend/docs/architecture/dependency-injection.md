# Sistema de Inyección de Dependencias

## Arquitectura Actual

El sistema utiliza **dependency-injector** integrado con **FastAPI** para proporcionar inyección de dependencias automática y type-safe.

## Componentes Principales

### 1. Container Central

```python
# core/fastapi/server/container_config.py
class CoreContainer(containers.DeclarativeContainer):
    """Container principal que incluye todos los módulos"""
    
    finance_container = providers.DependenciesContainer()
    auth_container = providers.DependenciesContainer()
    user_container = providers.DependenciesContainer()
    # ... otros containers
    
    def __init__(self):
        # Auto-registro de containers de módulos
        from modules.finance.container import FinanceContainer
        self.finance_container.override(FinanceContainer())
```

### 2. Dependencies Compartidas

```python
# shared/dependencies.py
@inject
def get_user_service(
    service = Provide["user_container.service"]
):
    return service

@inject
def get_currency_service(
    service = Provide["finance_container.currency_service"]
):
    return service
```

### 3. Uso en Endpoints

```python
# modules/user/adapter/input/api/v1/user.py
from shared.dependencies import get_user_service

@user_router.get("")
async def get_user_list(
    limit: int = Query(default=10),
    user_service = Depends(get_user_service),
):
    return await user_service.get_user_list(limit, page)
```

## Flujo de Resolución

```
FastAPI Request
    ↓
Depends(get_user_service)
    ↓
@inject decorator
    ↓
Provide["user_container.service"]
    ↓
CoreContainer.user_container
    ↓
UserContainer.service()
    ↓
UserService instance
```

## Configuración por Módulo

### Container del Módulo
```python
# modules/user/container.py
class UserContainer(DeclarativeContainer):
    repository = Singleton(UserSQLAlchemyRepository)
    service = Factory(UserService, repository=repository)
```

### Auto-registro
El container se registra automáticamente en `CoreContainer.__init__()`:

```python
try:
    from modules.user.container import UserContainer
    self.user_container.override(UserContainer())
except: 
    pass  # Módulo opcional
```

## Beneficios

### 1. **Type Safety**
- Resolución automática de tipos
- Validación en tiempo de compilación
- IntelliSense completo

### 2. **Performance**
- Lazy loading automático
- Singleton pattern integrado
- Cache de instancias

### 3. **Testing**
```python
# En tests
container.user_container.override(MockUserContainer())
```

### 4. **Error Handling**
- Errores claros de dependencias faltantes
- Validación automática de containers
- Fallback graceful para módulos opcionales

## Servicios Disponibles

### Módulo User
- `get_user_service()` - UserService

### Módulo Auth
- `get_auth_service()` - AuthService
- `get_jwt_service()` - JwtService

### Módulo RBAC
- `get_role_service()` - RoleService
- `get_permission_service()` - PermissionService

### Módulo Finance
- `get_currency_service()` - CurrencyService

### Módulo Provider
- `get_provider_service()` - ProviderService
- `get_draft_invoice_service()` - DraftPurchaseInvoiceService

### Módulo YiQi ERP
- `get_yiqi_service()` - YiqiService

### Módulo App Module
- `get_app_module_service()` - AppModuleService

### Módulo User Relationships
- `get_user_relationship_service()` - UserRelationshipService

## Agregar Nuevos Servicios

### 1. Crear Container del Módulo
```python
# modules/nuevo_modulo/container.py
class NuevoModuloContainer(DeclarativeContainer):
    repository = Singleton(NuevoRepository)
    service = Factory(NuevoService, repository=repository)
```

### 2. Registrar en CoreContainer
```python
# core/fastapi/server/container_config.py
class CoreContainer(DeclarativeContainer):
    nuevo_container = providers.DependenciesContainer()
    
    def __init__(self):
        try:
            from modules.nuevo_modulo.container import NuevoModuloContainer
            self.nuevo_container.override(NuevoModuloContainer())
        except: pass
```

### 3. Crear Dependency
```python
# shared/dependencies.py
@inject
def get_nuevo_service(
    service = Provide["nuevo_container.service"]
):
    return service
```

### 4. Usar en Endpoints
```python
@router.get("/endpoint")
async def endpoint(
    nuevo_service = Depends(get_nuevo_service)
):
    return await nuevo_service.do_something()
```

## Migración desde Service Locator

### Antes (Service Locator)
```python
def get_user_list():
    user_service = service_locator.get_service("user_service")
    if not user_service:
        return {"error": "Service not available"}
    return await user_service.get_user_list()
```

### Después (Dependency Injection)
```python
async def get_user_list(
    user_service = Depends(get_user_service)
):
    return await user_service.get_user_list()
```

## Ventajas del Sistema Actual

1. **Plug-and-Play**: Solo agregar container al CoreContainer
2. **Sin Boilerplate**: No más try/catch repetitivo
3. **Auto-wiring**: Resolución automática de dependencias
4. **Modular**: Cada módulo maneja sus propias dependencias
5. **Testeable**: Mock fácil para testing
6. **Type-Safe**: Validación automática de tipos

El sistema proporciona una base sólida para el crecimiento de la aplicación manteniendo la simplicidad y las mejores prácticas de dependency injection.