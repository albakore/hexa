# ¿Quién Crea y Mantiene los Protocols?

## Respuesta Corta

**El dueño del módulo que EXPONE el servicio es responsable de crear y mantener su Protocol.**

---

## Estructura Recomendada

Cada módulo que expone servicios debe tener su carpeta de protocols:

```
modules/user/
├── application/
│   ├── service/
│   │   └── user.py                           # ← Implementación
│   ├── protocols/                             # ← NUEVO
│   │   ├── __init__.py
│   │   └── user_service_protocol.py          # ← Protocol (API pública)
│   └── dto/
│       └── ...
```

```
modules/rbac/
├── application/
│   ├── service/
│   │   ├── role.py                            # ← Implementación
│   │   └── permission.py
│   ├── protocols/                             # ← NUEVO
│   │   ├── __init__.py
│   │   └── role_service_protocol.py          # ← Protocol (API pública)
│   └── dto/
│       └── ...
```

---

## Flujo de Creación

### 1. El Módulo Define Su Propia API

**Responsable**: Equipo del módulo `user`

```python
# modules/user/application/protocols/user_service_protocol.py
from typing import Protocol, Optional, Any

class UserServiceProtocol(Protocol):
    """
    API pública del módulo User.

    Mantenido por: Equipo de User
    """

    async def get_user_by_id(self, user_id: int) -> Optional[Any]:
        """Obtiene usuario por ID"""
        ...

    async def get_user_by_email(self, email: str) -> Optional[Any]:
        """Obtiene usuario por email"""
        ...
```

### 2. El Módulo Expone el Protocol

```python
# modules/user/application/protocols/__init__.py
from .user_service_protocol import UserServiceProtocol

__all__ = ["UserServiceProtocol"]
```

### 3. Otros Módulos Importan el Protocol (No el Servicio)

**Consumidor**: Módulo `auth`

```python
# modules/auth/application/service/auth.py
from modules.user.application.protocols import UserServiceProtocol  # ✅ Solo Protocol

class AuthService:
    def __init__(self, user_service: UserServiceProtocol):  # ✅ Type hint
        self.user_service = user_service

    async def login(self, email: str):
        # ✅ Autocompletado funciona
        user = await self.user_service.get_user_by_email(email)
```

---

## Ventajas de Este Enfoque

### ✅ 1. Separación de Responsabilidades Clara

```
Módulo User:
  ├── Define su implementación (UserService)
  ├── Define su API pública (UserServiceProtocol)
  └── Es dueño de ambas

Módulo Auth:
  ├── Consume la API pública (UserServiceProtocol)
  └── NO conoce la implementación
```

### ✅ 2. Protocol Vive Cerca de su Implementación

Cuando cambias `UserService`, el `UserServiceProtocol` está en la misma carpeta, facilitando mantenerlos sincronizados.

### ✅ 3. Versioning Claro

```python
# modules/user/application/protocols/
├── user_service_protocol.py       # API actual
└── user_service_protocol_v2.py    # Nueva versión (si es necesario)
```

### ✅ 4. Documentación Co-localizada

```python
class UserServiceProtocol(Protocol):
    """
    API pública del módulo User v1.0

    Changelog:
    - v1.0 (2025-10): Versión inicial

    Used by:
    - auth module (login, register)
    - admin module (user management)
    """
```

---

## Comparación: Protocols Centralizados vs Distribuidos

### ❌ Opción A: Protocols Centralizados (shared/)

```
shared/
└── interfaces/
    └── service_protocols.py  # ❌ Todos los protocols aquí
        ├── UserServiceProtocol
        ├── RoleServiceProtocol
        ├── ProductServiceProtocol
        └── ... (20+ protocols)
```

**Problemas**:
- ❌ Archivo gigante difícil de mantener
- ❌ No está claro quién es dueño de cada protocol
- ❌ Cambios en un protocol afectan archivo compartido
- ❌ Conflictos de merge frecuentes

### ✅ Opción B: Protocols Distribuidos (modules/**/protocols/)

```
modules/
├── user/
│   └── application/
│       └── protocols/
│           └── user_service_protocol.py      # ✅ Dueño: equipo User
├── rbac/
│   └── application/
│       └── protocols/
│           └── role_service_protocol.py      # ✅ Dueño: equipo RBAC
└── product/
    └── application/
        └── protocols/
            └── product_service_protocol.py    # ✅ Dueño: equipo Product
```

**Ventajas**:
- ✅ Cada equipo mantiene su propio protocol
- ✅ Cambios localizados, menos conflictos
- ✅ Ownership claro
- ✅ Fácil de navegar (protocol cerca de implementación)

---

## Workflow: Cambiar la API de un Módulo

### Escenario: User necesita añadir un nuevo método

**Paso 1**: Añadir método al servicio

```python
# modules/user/application/service/user.py
class UserService:
    async def get_users_by_role(self, role_id: int) -> List[User]:
        # Nueva funcionalidad
        return await self.repository.get_users_by_role(role_id)
```

**Paso 2**: Actualizar el protocol (mismo módulo)

```python
# modules/user/application/protocols/user_service_protocol.py
class UserServiceProtocol(Protocol):
    # ... métodos existentes ...

    async def get_users_by_role(self, role_id: int) -> List[Any]:  # ← NUEVO
        """Obtiene usuarios por rol"""
        ...
```

**Paso 3**: Los consumidores ahora ven el nuevo método

```python
# modules/admin/application/service/admin.py
from modules.user.application.protocols import UserServiceProtocol

class AdminService:
    def __init__(self, user_service: UserServiceProtocol):
        self.user_service = user_service

    async def get_admins(self):
        # ✅ IDE muestra el nuevo método en autocompletado
        return await self.user_service.get_users_by_role(1)
```

---

## Reglas de Oro

### ✅ DO

1. **Cada módulo define sus propios protocols** en `application/protocols/`
2. **Los protocols son parte de la API pública** del módulo
3. **Mantén protocol y servicio sincronizados**
4. **Documenta qué módulos usan cada método** (comentarios en el protocol)
5. **Usa nombres descriptivos** que reflejen el módulo: `UserServiceProtocol`, no `ServiceProtocol`

### ❌ DON'T

1. **No pongas todos los protocols en un archivo centralizado** (`shared/`)
2. **No importes la implementación concreta** (`UserService`) en otros módulos
3. **No dupliques protocols** (un protocol por servicio)
4. **No olvides actualizar el protocol** cuando cambies el servicio
5. **No uses `Any` en exceso** en los protocols (sé lo más específico posible)

---

## FAQ

### ¿Qué pasa con `shared/interfaces/service_protocols.py`?

**Respuesta**: Ese archivo se puede **deprecar** o usar solo para protocols **transversales** que NO pertenecen a un módulo específico.

**Mantener**:
```python
# shared/interfaces/service_protocols.py
# Solo para infraestructura compartida

class CacheServiceProtocol(Protocol):
    """Protocol para servicio de cache (no pertenece a ningún módulo)"""
    async def get(self, key: str) -> Any: ...
    async def set(self, key: str, value: Any) -> None: ...
```

**Mover a módulos**:
```python
# ❌ shared/interfaces/service_protocols.py
class UserServiceProtocol(Protocol): ...

# ✅ modules/user/application/protocols/user_service_protocol.py
class UserServiceProtocol(Protocol): ...
```

### ¿Los protocols pueden importar tipos de otros módulos?

**Sí, pero usa `Any` o tipos de `shared/`**:

```python
# ❌ Mal: Importa entidad de otro módulo
from modules.rbac.domain.entity import Role

class UserServiceProtocol(Protocol):
    async def get_user_with_role(self) -> Tuple[User, Role]:  # ❌
        ...

# ✅ Bien: Usa Any para evitar acoplamiento
from typing import Any, Tuple

class UserServiceProtocol(Protocol):
    async def get_user_with_role(self) -> Tuple[Any, Any]:  # ✅
        """Returns (User, Role)"""
        ...
```

### ¿Cómo valido que el servicio cumple con su protocol?

**Python valida automáticamente con duck typing**:

```python
# Si UserService tiene todos los métodos de UserServiceProtocol,
# entonces UserService "implements" UserServiceProtocol implícitamente

def func(service: UserServiceProtocol):
    # Acepta cualquier objeto con los métodos correctos
    pass

user_service = UserService()  # No hereda de UserServiceProtocol
func(user_service)  # ✅ Funciona! (structural subtyping)
```

Para validación explícita en tests:

```python
import pytest
from modules.user.application.service.user import UserService
from modules.user.application.protocols import UserServiceProtocol

def test_user_service_implements_protocol():
    """Verifica que UserService cumple con UserServiceProtocol"""
    service = UserService(repository=...)

    # Verifica que tiene todos los métodos
    assert hasattr(service, 'get_user_by_id')
    assert hasattr(service, 'get_user_by_email')
    assert callable(service.get_user_by_id)
```

---

## Checklist para Crear un Nuevo Protocol

- [ ] Crear carpeta `modules/{mi_modulo}/application/protocols/`
- [ ] Crear archivo `{servicio}_protocol.py`
- [ ] Definir `class {Servicio}Protocol(Protocol):`
- [ ] Añadir docstring con versión y changelog
- [ ] Listar todos los métodos públicos del servicio
- [ ] Documentar qué módulos usan cada método
- [ ] Crear `__init__.py` exportando el protocol
- [ ] Actualizar imports en módulos consumidores
- [ ] Ejecutar linter para verificar type checking

---

## Resumen

| Aspecto | Responsable | Ubicación |
|---------|-------------|-----------|
| **Crear Protocol** | Equipo dueño del módulo | `modules/{modulo}/application/protocols/` |
| **Mantener Protocol** | Equipo dueño del módulo | Junto con el servicio |
| **Usar Protocol** | Módulos consumidores | Import desde `modules/{modulo}/application/protocols/` |
| **Versionar Protocol** | Equipo dueño del módulo | Dentro del mismo módulo |

**Regla de Oro**: Si eres dueño del módulo `X`, eres dueño del `XServiceProtocol`.

---

**Fecha**: 2025-10-23
**Autor**: Arquitectura del Proyecto
