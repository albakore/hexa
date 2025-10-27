# Guía: Type-Safe Service Locator con Linter Support

## Problema

Cuando usas `service_locator.get_dependency()` o `service_locator.get_service()`, el linter (mypy, pyright, pylance) no puede inferir el tipo del servicio retornado, lo que resulta en pérdida de autocompletado y type checking.

```python
# ❌ Problema: user_service tiene tipo Any
user_service = service_locator.get_service("user_service")
# El linter no sabe qué métodos tiene user_service
```

## Solución: Protocols + Type Hints

Hemos implementado **3 estrategias** para lograr type-safety:

---

## Estrategia 1: Protocols en Type Hints (Recomendada) ⭐

### Paso 1: Definir Protocols

Los protocols ya están definidos en [`shared/interfaces/service_protocols.py`](shared/interfaces/service_protocols.py):

```python
from typing import Protocol, List, Optional, Any

class UserServiceProtocol(Protocol):
    """Define la API pública del UserService"""

    async def get_user_by_id(self, user_id: int) -> Optional[Any]:
        ...

    async def get_user_by_email_or_nickname(
        self, email: str, nickname: str, with_role: bool = False
    ) -> Optional[Any]:
        ...

    # ... más métodos
```

### Paso 2: Usar Protocols en Type Hints

En tu servicio (por ejemplo, `AuthService`):

```python
from shared.interfaces.service_protocols import UserServiceProtocol, RoleServiceProtocol

class AuthService:
    def __init__(
        self,
        auth_repository: AuthRepository,
        user_service: UserServiceProtocol,      # ✅ Type hint con Protocol
        role_service: RoleServiceProtocol,      # ✅ Type hint con Protocol
    ):
        self.user_service = user_service
        self.role_service = role_service

    async def login(self, email: str, password: str):
        # ✅ El linter ahora sabe que user_service tiene estos métodos
        user = await self.user_service.get_user_by_email_or_nickname(
            email=email, nickname=email
        )
        # ✅ Autocompletado funciona!
        permissions = await self.role_service.get_permissions_from_role(user.role)
```

### Ventajas
- ✅ **Autocompletado completo** en el IDE
- ✅ **Type checking** por mypy/pyright
- ✅ **Sin imports directos** entre módulos (solo el Protocol)
- ✅ **Duck typing**: No necesitas herencia, solo cumplir con la interfaz

### Ejemplo Real

Ver [`modules/auth/application/service/auth.py`](modules/auth/application/service/auth.py):

```python
from shared.interfaces.service_protocols import UserServiceProtocol, RoleServiceProtocol

class AuthService(AuthUseCase):
    def __init__(
        self,
        auth_repository: AuthRepository,
        user_service: UserServiceProtocol,  # ✅
        role_service: RoleServiceProtocol,  # ✅
    ):
        ...
```

---

## Estrategia 2: Métodos Type-Safe del ServiceLocator

### Método `get_typed_service()`

```python
from shared.interfaces.service_locator import service_locator
from shared.interfaces.service_protocols import UserServiceProtocol

# ✅ El linter sabe que user_service: UserServiceProtocol
user_service = service_locator.get_typed_service("user_service", UserServiceProtocol)

# Autocompletado funciona
user = await user_service.get_user_by_id(123)
```

### Método `get_typed_dependency()` (para FastAPI)

```python
from fastapi import APIRouter, Depends
from shared.interfaces.service_locator import service_locator
from shared.interfaces.service_protocols import UserServiceProtocol

router = APIRouter()

@router.get("/users/{user_id}")
async def get_user(
    user_id: int,
    user_service: UserServiceProtocol = Depends(
        service_locator.get_typed_dependency("user_service", UserServiceProtocol)
    )
):
    # ✅ user_service tiene type: UserServiceProtocol
    # ✅ Autocompletado funciona
    return await user_service.get_user_by_id(user_id)
```

---

## Estrategia 3: Type Annotations en Containers

En el container, puedes usar `cast` para ayudar al linter:

```python
from typing import cast
from shared.interfaces.service_locator import service_locator
from shared.interfaces.service_protocols import UserServiceProtocol

class AuthContainer(DeclarativeContainer):
    service = Factory(
        AuthService,
        auth_repository=repository_adapter,
        user_service=cast(
            UserServiceProtocol,
            service_locator.get_dependency("user_service")
        ),
    )
```

**Nota**: Esta estrategia es menos común porque el container ya inyecta dinámicamente.

---

## Configuración de Linters

### mypy (`pyproject.toml`)

```toml
[tool.mypy]
python_version = "3.11"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = false
check_untyped_defs = true

# Permite Protocols sin herencia explícita
enable_incomplete_feature = ["TypeVarTuple"]

# Ignora errores de dependency_injector (genera mucho ruido)
[[tool.mypy.overrides]]
module = "dependency_injector.*"
ignore_errors = true
```

### pylance (VSCode `settings.json`)

```json
{
  "python.analysis.typeCheckingMode": "basic",
  "python.analysis.diagnosticSeverityOverrides": {
    "reportGeneralTypeIssues": "warning",
    "reportOptionalMemberAccess": "warning"
  }
}
```

### pylint

```toml
[tool.pylint.typecheck]
# Ignora advertencias sobre atributos dinámicos
generated-members = ["service_locator.*"]
```

---

## Ejemplo Completo: De Principio a Fin

### 1. Definir Protocol (ya hecho)

```python
# shared/interfaces/service_protocols.py
from typing import Protocol, Optional, Any

class UserServiceProtocol(Protocol):
    async def get_user_by_id(self, user_id: int) -> Optional[Any]:
        ...
```

### 2. Implementar Servicio (ya existe)

```python
# modules/user/application/service/user.py
class UserService:  # No necesita heredar de UserServiceProtocol
    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        # Implementación...
```

### 3. Registrar en ServiceLocator (automático via module.py)

```python
# modules/user/module.py
@property
def service(self) -> Dict[str, object]:
    return {
        "user_service": self._container.service,
    }
```

### 4. Consumir con Type Safety

```python
# modules/auth/application/service/auth.py
from shared.interfaces.service_protocols import UserServiceProtocol

class AuthService:
    def __init__(
        self,
        auth_repository: AuthRepository,
        user_service: UserServiceProtocol,  # ✅ Type hint
    ):
        self.user_service = user_service

    async def login(self, email: str, password: str):
        # ✅ Autocompletado funciona
        user = await self.user_service.get_user_by_id(123)
```

### 5. Inyectar en Container

```python
# modules/auth/container.py
from shared.interfaces.service_locator import service_locator

class AuthContainer(DeclarativeContainer):
    service = Factory(
        AuthService,
        auth_repository=repository_adapter,
        user_service=service_locator.get_dependency("user_service"),  # ✅
    )
```

---

## Validación con Linters

### Comando para verificar tipos

```bash
# Con mypy
mypy backend/modules/auth/application/service/auth.py

# Con pyright
pyright backend/modules/auth/application/service/auth.py
```

### Resultado esperado

```bash
✅ Success: no issues found in 1 source file
```

### Detectar errores

Si intentas llamar un método que NO existe en el Protocol:

```python
# ❌ Error: UserServiceProtocol no tiene método 'delete_all'
await self.user_service.delete_all()
```

El linter mostrará:

```
error: "UserServiceProtocol" has no attribute "delete_all"  [attr-defined]
```

---

## Crear Nuevos Protocols

### Paso 1: Analizar el servicio

```bash
# Ver métodos públicos del servicio
grep -A 2 "async def" backend/modules/user/application/service/user.py
```

### Paso 2: Crear el Protocol

```python
# shared/interfaces/service_protocols.py
from typing import Protocol, List, Optional, Any

class MiNuevoServiceProtocol(Protocol):
    """Documentación del servicio"""

    async def metodo_1(self, param: int) -> Optional[Any]:
        """Descripción del método"""
        ...

    async def metodo_2(self, param: str) -> List[Any]:
        ...
```

### Paso 3: Usar en el consumidor

```python
from shared.interfaces.service_protocols import MiNuevoServiceProtocol

class OtroService:
    def __init__(self, mi_servicio: MiNuevoServiceProtocol):
        self.mi_servicio = mi_servicio
```

---

## Beneficios

### 1. Autocompletado en IDE

Cuando escribes `self.user_service.` el IDE te muestra todos los métodos disponibles.

### 2. Type Checking

```python
# ❌ Error detectado por linter
user = await self.user_service.get_user_by_id("abc")  # str en vez de int
# error: Argument 1 has incompatible type "str"; expected "int"
```

### 3. Refactoring Seguro

Si cambias la firma de un método en el Protocol, el linter te dirá dónde actualizar.

### 4. Documentación Auto-generada

Los IDEs pueden generar documentación automática desde los Protocols.

---

## Troubleshooting

### "Cannot find reference 'get_user_by_id' in 'Any'"

**Problema**: No estás usando el type hint con Protocol.

**Solución**: Añade el type hint:
```python
def __init__(self, user_service: UserServiceProtocol):  # ← Añadir esto
```

### "Module has no attribute 'UserServiceProtocol'"

**Problema**: Falta importar el Protocol.

**Solución**:
```python
from shared.interfaces.service_protocols import UserServiceProtocol
```

### "Protocol 'UserServiceProtocol' cannot be instantiated"

**Problema**: Estás intentando crear una instancia del Protocol.

**Solución**: Los Protocols solo son para type hints, no se instancian:
```python
# ❌ Mal
service = UserServiceProtocol()

# ✅ Bien
service = service_locator.get_typed_service("user_service", UserServiceProtocol)
```

---

## Resumen

| Estrategia | Dónde usar | Ventajas | IDE Support |
|------------|-----------|----------|-------------|
| **Protocol Type Hints** | Constructores de servicios | Simple, type-safe | ⭐⭐⭐⭐⭐ |
| **get_typed_service()** | Obtención manual | Explícito | ⭐⭐⭐⭐ |
| **get_typed_dependency()** | FastAPI endpoints | Type-safe en Depends | ⭐⭐⭐⭐⭐ |
| **cast()** | Containers | Ayuda al linter | ⭐⭐⭐ |

**Recomendación**: Usa **Protocol Type Hints** en constructores (Estrategia 1) para máxima claridad y soporte del linter.

---

## Archivos Relacionados

- [`shared/interfaces/service_protocols.py`](shared/interfaces/service_protocols.py) - Definiciones de Protocols
- [`shared/interfaces/service_locator.py`](shared/interfaces/service_locator.py) - ServiceLocator mejorado
- [`modules/auth/application/service/auth.py`](modules/auth/application/service/auth.py) - Ejemplo de uso

---

**Fecha**: 2025-10-23
**Versión**: 1.0
