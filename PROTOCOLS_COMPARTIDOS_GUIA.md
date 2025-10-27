# Guía de Protocols Compartidos

## Ubicación Centralizada

Todos los protocols de servicios se encuentran en un único archivo:

**[`shared/interfaces/service_protocols.py`](shared/interfaces/service_protocols.py)**

Este archivo contiene los protocols para **todos los módulos del sistema**.

---

## ¿Por qué Centralizado?

### Ventajas

✅ **Un solo archivo para todos los protocols**: Fácil de encontrar y mantener
✅ **Compartido entre todos los módulos**: No hay duplicación
✅ **Fácil navegación**: Todo en un solo lugar
✅ **Menos archivos**: Estructura más simple
✅ **IDE friendly**: Importaciones simples desde un solo lugar

### Estructura del Archivo

```python
# shared/interfaces/service_protocols.py

# ============================================================================
# USER MODULE
# ============================================================================
class UserServiceProtocol(Protocol):
    """API pública del módulo User"""
    ...

# ============================================================================
# RBAC MODULE
# ============================================================================
class RoleServiceProtocol(Protocol):
    """API pública del módulo RBAC"""
    ...

class PermissionServiceProtocol(Protocol):
    """API pública del módulo RBAC"""
    ...

# ============================================================================
# FILE STORAGE MODULE
# ============================================================================
class FileStorageServiceProtocol(Protocol):
    """API pública del módulo FileStorage"""
    ...

# ... y así sucesivamente para cada módulo
```

---

## Protocols Disponibles

El archivo contiene protocols para **15 módulos**:

| Protocol | Módulo | Descripción |
|----------|--------|-------------|
| `UserServiceProtocol` | user | Gestión de usuarios |
| `RoleServiceProtocol` | rbac | Gestión de roles |
| `PermissionServiceProtocol` | rbac | Gestión de permisos |
| `AppModuleServiceProtocol` | module | Gestión de módulos de aplicación |
| `FileStorageServiceProtocol` | file_storage | Gestión de archivos S3 |
| `CurrencyServiceProtocol` | finance | Gestión de monedas |
| `YiqiServiceProtocol` | yiqi_erp | Integración con ERP externo |
| `ProviderServiceProtocol` | provider | Gestión de proveedores |
| `DraftPurchaseInvoiceServiceProtocol` | provider | Borradores de facturas |
| `PurchaseInvoiceServiceTypeServiceProtocol` | provider | Tipos de servicio |
| `PurchaseInvoiceServiceProtocol` | invoicing | Facturas de compra |
| `AuthServiceProtocol` | auth | Autenticación |
| `JwtServiceProtocol` | auth | JWT tokens |

---

## Cómo Usar

### 1. Importar el Protocol

```python
# En cualquier módulo que necesite usar otro servicio
from shared.interfaces.service_protocols import UserServiceProtocol, RoleServiceProtocol
```

### 2. Usar como Type Hint

```python
class AuthService:
    def __init__(
        self,
        auth_repository: AuthRepository,
        user_service: UserServiceProtocol,      # ✅ Type hint con Protocol
        role_service: RoleServiceProtocol,      # ✅ Type hint con Protocol
    ):
        self.user_service = user_service
        self.role_service = role_service

    async def login(self, email: str):
        # ✅ Autocompletado funciona!
        user = await self.user_service.get_user_by_email_or_nickname(email, email)

        # ✅ Linter detecta errores
        permissions = await self.role_service.get_permissions_from_role(user.role)
```

### 3. Configurar en Container

```python
# modules/auth/container.py
from shared.interfaces.service_locator import service_locator

class AuthContainer(DeclarativeContainer):
    service = Factory(
        AuthService,
        auth_repository=repository_adapter,
        user_service=service_locator.get_dependency("user_service"),
        role_service=service_locator.get_dependency("rbac.role_service"),
    )
```

---

## Ejemplo Completo

### Paso 1: Ver el Protocol Disponible

```python
# shared/interfaces/service_protocols.py

class UserServiceProtocol(Protocol):
    async def get_user_by_id(self, user_id: int) -> Optional[Any]:
        """Obtiene usuario por ID"""
        ...

    async def get_user_by_email_or_nickname(
        self, email: str, nickname: str, with_role: bool = False
    ) -> Optional[Any]:
        """Obtiene usuario por email o nickname"""
        ...
```

### Paso 2: Usar en tu Servicio

```python
# modules/auth/application/service/auth.py
from shared.interfaces.service_protocols import UserServiceProtocol, RoleServiceProtocol

class AuthService:
    def __init__(
        self,
        auth_repository: AuthRepository,
        user_service: UserServiceProtocol,  # ✅ Import desde shared
        role_service: RoleServiceProtocol,  # ✅ Import desde shared
    ):
        self.user_service = user_service
        self.role_service = role_service
```

### Paso 3: Disfrutar del Autocompletado

```python
async def login(self, email: str, password: str):
    # Cuando escribes "self.user_service." el IDE te muestra:
    # - get_user_by_id
    # - get_user_by_email_or_nickname
    # - save_user
    # - set_user_password
    # - create_user
    # - asign_role_to_user
    # - get_all_user_with_roles

    user = await self.user_service.get_user_by_email_or_nickname(
        email=email,
        nickname=email,
        with_role=True
    )
```

---

## Mantenimiento

### ¿Cuándo actualizar un Protocol?

Actualiza el protocol cuando:
1. Añades un nuevo método público al servicio
2. Cambias la firma de un método existente
3. Cambias el tipo de retorno
4. Añades/remueves parámetros

### ¿Quién actualiza el Protocol?

**El equipo que modifica el servicio es responsable de actualizar su protocol correspondiente.**

### Workflow

1. **Modificas el servicio**:
   ```python
   # modules/user/application/service/user.py
   class UserService:
       async def get_users_by_status(self, status: str) -> List[User]:  # NUEVO
           return await self.repository.get_by_status(status)
   ```

2. **Actualizas el protocol**:
   ```python
   # shared/interfaces/service_protocols.py
   class UserServiceProtocol(Protocol):
       # ... métodos existentes ...

       async def get_users_by_status(self, status: str) -> List[Any]:  # NUEVO
           """Obtiene usuarios por estado"""
           ...
   ```

3. **Los consumidores automáticamente ven el cambio**:
   ```python
   # modules/admin/application/service/admin.py
   async def get_active_users(self):
       # ✅ IDE ahora muestra el nuevo método
       return await self.user_service.get_users_by_status("active")
   ```

---

## Convenciones

### Nombres de Protocols

```python
# ✅ Correcto
class UserServiceProtocol(Protocol): ...
class RoleServiceProtocol(Protocol): ...
class FileStorageServiceProtocol(Protocol): ...

# ❌ Incorrecto
class UserProtocol(Protocol): ...  # Falta "Service"
class IUserService(Protocol): ...  # No usar prefijo "I"
```

### Documentación en Protocols

Cada método debe tener:
- **Docstring**: Qué hace el método
- **Used by**: Qué módulos lo usan (opcional pero útil)

```python
class UserServiceProtocol(Protocol):
    async def get_user_by_email_or_nickname(
        self, email: str, nickname: str, with_role: bool = False
    ) -> Optional[Any]:
        """
        Obtiene usuario por email o nickname.

        Args:
            email: Email del usuario
            nickname: Nickname del usuario
            with_role: Si debe incluir información del rol

        Used by: auth (login, register)
        """
        ...
```

### Tipos en Protocols

Usa `Any` para tipos complejos que pertenecen a otros módulos:

```python
# ✅ Correcto
class UserServiceProtocol(Protocol):
    async def get_user_by_id(self, user_id: int) -> Optional[Any]:  # Any en vez de User
        ...

# ❌ Incorrecto (crea dependencia)
from modules.user.domain.entity import User

class UserServiceProtocol(Protocol):
    async def get_user_by_id(self, user_id: int) -> Optional[User]:  # ❌
        ...
```

---

## Ventajas del Linter

### 1. Autocompletado

Cuando escribes `self.user_service.` el IDE muestra todos los métodos:

```python
self.user_service.
# ↓ Aparece:
# - get_user_by_id
# - get_user_by_email_or_nickname
# - save_user
# - ...
```

### 2. Detección de Errores

```python
# ❌ Error: tipo incorrecto
user = await self.user_service.get_user_by_id("abc")  # str en vez de int
# error: Argument 1 has incompatible type "str"; expected "int"

# ❌ Error: método no existe
user = await self.user_service.delete_all_users()
# error: "UserServiceProtocol" has no attribute "delete_all_users"
```

### 3. Documentación en Hover

Cuando pasas el mouse sobre un método, el IDE muestra la documentación:

```python
user = await self.user_service.get_user_by_id(123)
#                               ↑ Hover aquí muestra: "Obtiene usuario por ID"
```

---

## FAQ

### ¿Debo crear un protocol para cada servicio?

**Sí**, cada servicio que sea usado por otros módulos debe tener su protocol en `shared/interfaces/service_protocols.py`.

### ¿Y si mi servicio solo se usa internamente?

Si tu servicio **NO** es usado por otros módulos, no necesitas un protocol. Los protocols son solo para la **API pública** entre módulos.

### ¿Puedo tener varios protocols para un mismo módulo?

**Sí**, si un módulo expone varios servicios:

```python
# shared/interfaces/service_protocols.py

# RBAC tiene 2 servicios
class RoleServiceProtocol(Protocol): ...
class PermissionServiceProtocol(Protocol): ...

# Provider tiene 3 servicios
class ProviderServiceProtocol(Protocol): ...
class DraftPurchaseInvoiceServiceProtocol(Protocol): ...
class PurchaseInvoiceServiceTypeServiceProtocol(Protocol): ...
```

### ¿El protocol debe tener TODOS los métodos del servicio?

**No**, solo los métodos que son parte de la **API pública** (los que otros módulos usan).

Métodos privados o internos no van en el protocol:

```python
class UserService:
    # ✅ En protocol (público)
    async def get_user_by_id(self, user_id: int):
        ...

    # ❌ NO en protocol (privado)
    def _validate_user_data(self, user):
        ...
```

### ¿Cómo actualizo el protocol cuando cambio el servicio?

1. Modifica el servicio
2. Ejecuta mypy/pyright
3. El linter te dirá dónde actualizar el protocol
4. Actualiza el protocol en `shared/interfaces/service_protocols.py`

---

## Resumen

| Aspecto | Ubicación | Responsable |
|---------|-----------|-------------|
| **Protocols** | `shared/interfaces/service_protocols.py` | Todos (centralizado) |
| **Mantener sincronizado** | Al modificar servicio | Equipo que modifica el servicio |
| **Importar** | `from shared.interfaces.service_protocols import ...` | Módulos consumidores |
| **Type hints** | En constructores de servicios | Todos los servicios |

**Ventaja clave**: Un solo archivo para todas las APIs públicas del sistema.

---

## Archivos Relacionados

- **[`shared/interfaces/service_protocols.py`](shared/interfaces/service_protocols.py)** - Todos los protocols
- **[`shared/interfaces/service_locator.py`](shared/interfaces/service_locator.py)** - ServiceLocator con métodos type-safe
- **[`GUIA_TYPE_SAFE_SERVICE_LOCATOR.md`](GUIA_TYPE_SAFE_SERVICE_LOCATOR.md)** - Guía de uso del ServiceLocator
- **[`modules/auth/application/service/auth.py`](modules/auth/application/service/auth.py)** - Ejemplo de uso

---

**Fecha**: 2025-10-23
**Enfoque**: Protocols Centralizados en `shared/`
