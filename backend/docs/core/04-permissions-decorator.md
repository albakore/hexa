# Sistema de Permisos con Decoradores

Este documento explica cómo usar el sistema de permisos basado en decoradores implementado en el proyecto.

## 📋 Índice

1. [Arquitectura](#arquitectura)
2. [Uso del decorador](#uso-del-decorador)
3. [Ejemplos](#ejemplos)
4. [Respuestas de error](#respuestas-de-error)
5. [Integración con el sistema existente](#integración-con-el-sistema-existente)

---

## Arquitectura

El sistema de permisos consta de tres componentes principales:

### 1. **AuthenticationMiddleware**
Ubicación: `core/fastapi/middlewares/authentication.py`

- Valida el token JWT del header `Authorization`
- Extrae el usuario y sus permisos
- Los permisos se cargan desde la sesión del usuario en la base de datos
- Inyecta `request.user` con la información del usuario autenticado

```python
# En AuthBackend.authenticate()
user.permissions = session.permissions  # Lista de tokens: ["invoices:read", "users:write"]
```

### 2. **PermissionValidationMiddleware**
Ubicación: `core/fastapi/middlewares/permissions.py`

- Se ejecuta DESPUÉS de `AuthenticationMiddleware`
- Lee el atributo `__required_permissions__` del endpoint
- Compara los permisos del usuario con los permisos requeridos
- Si faltan permisos, retorna `403 Forbidden`
- Si tiene todos los permisos, continúa con la ejecución

### 3. **@require_permissions Decorator**
Ubicación: `core/fastapi/decorators/permissions.py`

- Decorador que marca endpoints con permisos requeridos
- Almacena los permisos en el atributo `__required_permissions__` de la función
- El middleware lee este atributo para validar

---

## Uso del decorador

### Sintaxis básica

```python
from fastapi import APIRouter
from core.fastapi.decorators import require_permissions

router = APIRouter()

@router.get("/endpoint")
@require_permissions("resource:action")
async def my_endpoint():
    return {"message": "Success"}
```

### Múltiples permisos (AND)

El decorador valida que el usuario tenga **TODOS** los permisos especificados:

```python
@router.post("/invoices")
@require_permissions("invoices:create", "invoices:write")
async def create_invoice():
    # El usuario DEBE tener ambos permisos: invoices:create Y invoices:write
    return {"created": True}
```

---

## Ejemplos

### Ejemplo 1: CRUD de Purchase Invoices

```python
from fastapi import APIRouter, Depends
from core.fastapi.decorators import require_permissions
from modules.invoicing.application.service.purchase_invoice import PurchaseInvoiceService

purchase_invoice_router = APIRouter(prefix="/purchase_invoices", tags=["Purchase Invoices"])


@purchase_invoice_router.get("")
@require_permissions("invoices:read")
async def get_all_purchase_invoices(
    limit: int = 50,
    page: int = 0,
    service: PurchaseInvoiceService = Depends(...)
):
    """Lista todas las facturas - requiere permiso de lectura"""
    return await service.get_list(limit, page)


@purchase_invoice_router.get("/{invoice_id}")
@require_permissions("invoices:read")
async def get_purchase_invoice(
    invoice_id: int,
    service: PurchaseInvoiceService = Depends(...)
):
    """Obtiene una factura específica - requiere permiso de lectura"""
    return await service.get_one_by_id(invoice_id)


@purchase_invoice_router.post("")
@require_permissions("invoices:create", "invoices:write")
async def create_purchase_invoice(
    data: CreatePurchaseInvoiceRequest,
    service: PurchaseInvoiceService = Depends(...)
):
    """Crea una factura - requiere permisos de creación y escritura"""
    return await service.create(data)


@purchase_invoice_router.put("/{invoice_id}")
@require_permissions("invoices:update", "invoices:write")
async def update_purchase_invoice(
    invoice_id: int,
    data: UpdatePurchaseInvoiceRequest,
    service: PurchaseInvoiceService = Depends(...)
):
    """Actualiza una factura - requiere permisos de actualización y escritura"""
    return await service.update(invoice_id, data)


@purchase_invoice_router.delete("/{invoice_id}")
@require_permissions("invoices:delete", "invoices:admin")
async def delete_purchase_invoice(
    invoice_id: int,
    service: PurchaseInvoiceService = Depends(...)
):
    """Elimina una factura - requiere permisos de eliminación y admin"""
    return await service.delete(invoice_id)


@purchase_invoice_router.post("/{invoice_id}/emit")
@require_permissions("invoices:emit", "invoices:write")
async def emit_purchase_invoice(
    invoice_id: int,
    service: PurchaseInvoiceService = Depends(...)
):
    """Emite una factura - requiere permisos de emisión y escritura"""
    return await service.emit(invoice_id)
```

### Ejemplo 2: Endpoint público (sin permisos)

Algunos endpoints no requieren permisos específicos, solo autenticación:

```python
@router.get("/profile")
async def get_my_profile(request: Request):
    """
    Obtiene el perfil del usuario autenticado.

    No requiere @require_permissions porque solo necesita estar autenticado.
    El AuthenticationMiddleware ya validó que tiene un token válido.
    """
    return {
        "id": request.user.id,
        "email": request.user.email,
        "nickname": request.user.nickname
    }
```

### Ejemplo 3: Endpoint completamente público

Para endpoints que no requieren ni autenticación:

```python
@router.get("/health")
async def health_check():
    """
    Health check endpoint - completamente público.

    No requiere autenticación ni permisos.
    """
    return {"status": "healthy"}
```

---

## Respuestas de error

### 401 Unauthorized - No autenticado

Cuando no hay token o el token es inválido:

```json
{
  "error_code": "UNAUTHORIZED",
  "message": "Not authenticated"
}
```

### 403 Forbidden - Sin permisos

Cuando el usuario está autenticado pero no tiene los permisos necesarios:

```json
{
  "error_code": "FORBIDDEN",
  "message": "Missing required permissions: invoices:create, invoices:write",
  "required_permissions": ["invoices:create", "invoices:write"],
  "missing_permissions": ["invoices:create"]
}
```

En este ejemplo:
- El usuario tiene el permiso `invoices:write`
- Pero le falta `invoices:create`
- Por lo tanto, el acceso es denegado

---

## Integración con el sistema existente

### PermissionGroup (Sistema existente)

El sistema ya tiene `PermissionGroup` para definir permisos:

```python
# modules/invoicing/permissions.py
from core.fastapi.dependencies.permission import PermissionGroup

class InvoicingPermissions(PermissionGroup):
    group = "invoices"

    read = "Ver facturas"
    create = "Crear facturas"
    update = "Actualizar facturas"
    delete = "Eliminar facturas"
    write = "Escribir facturas"
    emit = "Emitir facturas"
    admin = "Administrar facturas"
```

Esto genera automáticamente los tokens:
- `invoices:read`
- `invoices:create`
- `invoices:update`
- etc.

### Usar con el decorador

```python
from core.fastapi.decorators import require_permissions
from modules.invoicing.permissions import InvoicingPermissions

@router.get("/invoices")
@require_permissions("invoices:read")  # Usar el token directamente
async def get_invoices():
    return {"invoices": []}
```

### Ventajas del decorador vs PermissionDependency

#### PermissionDependency (sistema anterior):
```python
@router.get("/invoices")
async def get_invoices(
    _: None = InvoicingPermissions.read  # Inyecta como dependencia
):
    return {"invoices": []}
```

**Ventajas:**
- Integrado con Swagger (aparece en la documentación)
- Tipo de validación explícita

**Desventajas:**
- Verbose (requiere parámetro extra)
- No permite múltiples permisos fácilmente

#### @require_permissions (nuevo sistema):
```python
@router.get("/invoices")
@require_permissions("invoices:read")
async def get_invoices():
    return {"invoices": []}
```

**Ventajas:**
- Limpio y conciso
- Soporta múltiples permisos fácilmente: `@require_permissions("a", "b", "c")`
- No contamina la firma de la función

**Desventajas:**
- No aparece automáticamente en Swagger (se puede agregar manualmente)

### Puedes usar ambos

Los dos sistemas son compatibles. Puedes usar el que prefieras según el caso:

```python
# Opción 1: Decorador (recomendado para múltiples permisos)
@router.post("/invoices")
@require_permissions("invoices:create", "invoices:write")
async def create_invoice(data: InvoiceData):
    return {"created": True}

# Opción 2: Dependency (útil para Swagger documentation)
@router.get("/invoices")
async def get_invoices(_: None = InvoicingPermissions.read):
    return {"invoices": []}
```

---

## Stack de middlewares

Orden de ejecución de los middlewares (importante):

```python
# core/fastapi/server/__init__.py
def make_middleware():
    middleware = [
        Middleware(CORSMiddleware),           # 1. Valida CORS
        Middleware(AuthenticationMiddleware),  # 2. Valida JWT y carga request.user
        Middleware(PermissionValidationMiddleware),  # 3. Valida permisos del decorador
        Middleware(SQLAlchemyMiddleware),     # 4. Maneja sesiones de DB
    ]
    return middleware
```

**Importante**: `PermissionValidationMiddleware` DEBE estar después de `AuthenticationMiddleware` para que `request.user` ya esté disponible.

---

## Testing

### Ejemplo de test con permisos

```python
import pytest
from fastapi.testclient import TestClient

def test_endpoint_with_permission(client: TestClient, auth_token):
    """Usuario con permisos correctos"""
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.get("/invoices", headers=headers)
    assert response.status_code == 200

def test_endpoint_without_permission(client: TestClient, auth_token_no_perms):
    """Usuario sin permisos"""
    headers = {"Authorization": f"Bearer {auth_token_no_perms}"}
    response = client.get("/invoices", headers=headers)
    assert response.status_code == 403
    assert "missing_permissions" in response.json()

def test_endpoint_unauthenticated(client: TestClient):
    """Sin autenticación"""
    response = client.get("/invoices")
    assert response.status_code == 401
```

---

## Resumen

✅ **Usa el decorador cuando:**
- Necesitas múltiples permisos (AND)
- Quieres código limpio sin parámetros extra
- Los permisos son claros y no necesitan aparecer en Swagger

✅ **Usa PermissionDependency cuando:**
- Solo necesitas un permiso
- Quieres que aparezca automáticamente en Swagger
- Prefieres el sistema de inyección de dependencias de FastAPI

✅ **No uses ninguno cuando:**
- El endpoint es completamente público (ej: health check)
- Solo necesitas autenticación básica (ya la da `AuthenticationMiddleware`)