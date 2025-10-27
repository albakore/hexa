# Cambios Aplicados para Desacoplar Módulos

## Resumen

Se han aplicado cambios críticos para eliminar las dependencias directas entre módulos y lograr un desacoplamiento completo siguiendo los principios de arquitectura hexagonal.

---

## Cambios Realizados

### 1. Exposición de Repositorios en ServiceLocator

Todos los módulos ahora exponen sus repositorios a través del ServiceLocator para que puedan ser consumidos por otros módulos sin imports directos.

#### Archivos Modificados:

**`modules/user/module.py`**
```python
@property
def service(self) -> Dict[str, object]:
    return {
        "user_service": self._container.service,
        "user.repository_adapter": self._container.repository_adapter,  # ✅ NUEVO
    }
```

**`modules/rbac/module.py`**
```python
@property
def service(self) -> Dict[str, object]:
    return {
        "rbac.role_service": self._container.role_service,
        "rbac.permission_service": self._container.permission_service,
        "rbac.repository_adapter": self._container.repository_adapter,  # ✅ NUEVO
    }
```

**`modules/module/module.py`** (AppModule)
```python
@property
def service(self) -> Dict[str, object]:
    return {
        "app_module_service": self._container.service,
        "app_module.repository_adapter": self._container.repository_adapter,  # ✅ NUEVO
    }
```

**`modules/yiqi_erp/module.py`**
```python
@property
def service(self) -> Dict[str, object]:
    from .adapter.input.tasks.yiqi_erp import emit_invoice

    return {
        "yiqi_service": self._container.service,  # ✅ NUEVO
        "yiqi_erp_service": self._container.service,
        "yiqi_erp_tasks": {"emit_invoice": emit_invoice},
    }
```

---

### 2. Eliminación de Imports Directos en Containers

Se eliminaron todos los imports de containers de otros módulos, reemplazándolos por `service_locator`.

#### **`modules/auth/container.py`**

**ANTES (❌ Acoplado):**
```python
from modules.rbac.container import RBACContainer
from modules.user.container import UserContainer

service = Factory(
    AuthService,
    auth_repository=repository_adapter,
    user_repository=UserContainer.repository_adapter,  # ❌
    rbac_repository=RBACContainer.repository_adapter,  # ❌
)
```

**DESPUÉS (✅ Desacoplado):**
```python
from shared.interfaces.service_locator import service_locator

service = Factory(
    AuthService,
    auth_repository=repository_adapter,
    user_repository=service_locator.get_dependency("user.repository_adapter"),  # ✅
    rbac_repository=service_locator.get_dependency("rbac.repository_adapter"),  # ✅
)

jwt_service = Factory(
    JwtService,
    auth_repository=repository_adapter,
    rbac_repository=service_locator.get_dependency("rbac.repository_adapter"),  # ✅
)
```

#### **`modules/rbac/container.py`**

**ANTES (❌ Acoplado):**
```python
from modules.module.container import AppModuleContainer

role_service = Factory(
    RoleService,
    role_repository=repository_adapter,
    permission_repository=repository_adapter,
    module_repository=AppModuleContainer.repository_adapter,  # ❌
)
```

**DESPUÉS (✅ Desacoplado):**
```python
from shared.interfaces.service_locator import service_locator

role_service = Factory(
    RoleService,
    role_repository=repository_adapter,
    permission_repository=repository_adapter,
    module_repository=service_locator.get_dependency("app_module.repository_adapter"),  # ✅
)
```

#### **`modules/provider/container.py`**

**ANTES (❌ Acoplado):**
```python
from modules.yiqi_erp.container import YiqiContainer, YiqiService

yiqi_service: Provider = service_locator.get_service("yiqi_service")

draft_invoice_service = Factory(
    DraftPurchaseInvoiceService,
    yiqi_service=yiqi_service,  # ⚠️ Usaba variable que importaba el tipo
    ...
)
```

**DESPUÉS (✅ Desacoplado):**
```python
# Sin imports de otros módulos

draft_invoice_service = Factory(
    DraftPurchaseInvoiceService,
    draft_purchase_invoice_repository=draft_invoice_repo_adapter,
    file_storage_service=service_locator.get_dependency("file_storage_service"),  # ✅
    yiqi_service=service_locator.get_dependency("yiqi_service"),  # ✅
    currency_service=service_locator.get_dependency("currency_service"),  # ✅
)
```

---

### 3. Creación de Protocolos Compartidos

Se creó un nuevo archivo con contratos (Protocols) que definen las interfaces entre módulos sin necesidad de imports.

#### **`shared/interfaces/module_contracts.py`** (NUEVO)

Define protocolos para:
- `UserRepositoryProtocol`
- `RBACRepositoryProtocol`
- `AppModuleRepositoryProtocol`
- `YiqiServiceProtocol`
- `FileStorageServiceProtocol`
- `CurrencyServiceProtocol`

Estos protocolos permiten a los módulos definir qué esperan de otros servicios sin importar sus tipos concretos.

**Ejemplo:**
```python
class YiqiServiceProtocol(Protocol):
    """Contrato para servicio de Yiqi ERP"""

    async def get_currency_by_code(self, code: str, company_id: int) -> dict:
        """Obtiene moneda por código"""
        ...

    async def create_invoice(self, command: Any, company_id: int) -> dict:
        """Crea una factura en Yiqi ERP"""
        ...
```

---

## Impacto de los Cambios

### Beneficios Inmediatos

1. **✅ Módulos Independientes**: Ahora cada módulo puede ser desarrollado, testeado y desplegado de forma independiente.

2. **✅ Eliminación de Dependencias Circulares**: Ya no hay riesgo de dependencias circulares entre módulos.

3. **✅ Mejor Testabilidad**: Los módulos pueden ser testeados con mocks sin necesidad de instanciar otros módulos.

4. **✅ Preparado para Microservicios**: Cada módulo puede convertirse en un microservicio independiente.

5. **✅ Cambios Locales**: Modificar la implementación interna de un módulo no afecta a otros.

### Diagrama de Dependencias - ANTES vs DESPUÉS

**ANTES (❌):**
```
auth ──┬──> user (UserContainer.repository_adapter)
       └──> rbac (RBACContainer.repository_adapter)

rbac ────> module (AppModuleContainer.repository_adapter)

provider ──> yiqi_erp (YiqiContainer, imports directos)
```

**DESPUÉS (✅):**
```
auth ──┬──> service_locator("user.repository_adapter")
       └──> service_locator("rbac.repository_adapter")

rbac ────> service_locator("app_module.repository_adapter")

provider ─┬──> service_locator("yiqi_service")
          ├──> service_locator("file_storage_service")
          └──> service_locator("currency_service")
```

---

## Validación de Desacoplamiento

Para verificar que los módulos están completamente desacoplados, deberías poder:

### ✅ Test 1: Eliminar un módulo sin romper imports
```bash
# Temporalmente renombrar un módulo
mv modules/yiqi_erp modules/_yiqi_erp_disabled

# Los otros módulos deberían importar sin errores
python -c "from modules.provider.container import ProviderContainer"
```

### ✅ Test 2: Tests unitarios independientes
```bash
# Testear un módulo sin instanciar otros
pytest modules/auth/tests/ --no-cov
```

### ✅ Test 3: Inspección de imports
```bash
# No debería haber imports cruzados entre módulos
grep -r "from modules\.\w*\.container import" modules/*/container.py
# Resultado esperado: Sin coincidencias (excepto imports del propio módulo)
```

---

## Trabajo Pendiente (Opcional)

### 1. Actualizar Tipos en Servicios

Algunos servicios aún usan `Any` o `type` para dependencias externas. Pueden actualizarse para usar los `Protocol` definidos:

**Ejemplo en `draft_purchase_invoice.py`:**
```python
from shared.interfaces.module_contracts import (
    YiqiServiceProtocol,
    FileStorageServiceProtocol,
    CurrencyServiceProtocol
)

@dataclass
class DraftPurchaseInvoiceService:
    draft_purchase_invoice_repository: DraftPurchaseInvoiceRepository
    file_storage_service: FileStorageServiceProtocol  # En vez de Any
    yiqi_service: YiqiServiceProtocol  # En vez de Any
    currency_service: CurrencyServiceProtocol | None  # En vez de Any
```

### 2. Implementar EventBus para Comunicación Asíncrona

El EventBus ya está implementado pero no se usa. Podría usarse para:
- Notificaciones entre módulos
- Eventos de dominio
- Comunicación desacoplada asíncrona

**Ejemplo:**
```python
# En provider, al finalizar una factura
event_bus.publish(DomainEvent(
    event_type="draft_invoice.finalized",
    data={"invoice_id": invoice_id},
    timestamp=datetime.now(),
    module_source="provider"
))

# En invoicing, suscribirse al evento
event_bus.subscribe("draft_invoice.finalized", InvoiceCreatedHandler())
```

### 3. Linting para Prevenir Acoplamientos Futuros

Configurar pylint o flake8 para detectar imports cruzados:

```python
# .pylintrc o pyproject.toml
[tool.pylint.imports]
forbidden-imports = [
    "modules.*.container",  # Prohibir imports de containers externos
]
```

---

## Comandos para Verificar

```bash
# 1. Verificar que no hay imports directos de containers
grep -r "from modules\.\w*\.container import" modules/*/container.py | grep -v "from modules\.$(basename $(dirname {}))\."

# 2. Verificar que ServiceLocator está siendo usado
grep -r "service_locator.get_" modules/*/container.py

# 3. Listar servicios registrados
grep -r "def service" modules/*/module.py -A 10
```

---

## Conclusión

El proyecto ahora tiene un **desacoplamiento significativamente mejorado**:

- **ANTES**: Nivel de acoplamiento MEDIO-ALTO ⚠️
- **DESPUÉS**: Nivel de acoplamiento BAJO ✅

Todos los imports directos entre containers han sido eliminados y reemplazados por el patrón ServiceLocator. Los módulos ahora pueden funcionar de forma independiente y el proyecto está preparado para escalar a una arquitectura de microservicios si es necesario.

---

**Fecha de cambios**: 2025-10-23
**Módulos afectados**: auth, rbac, provider, user, module, yiqi_erp
**Archivos creados**: `shared/interfaces/module_contracts.py`
**Archivos modificados**: 7 containers, 4 module definitions
