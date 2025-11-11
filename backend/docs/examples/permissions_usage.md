# Uso del sistema de permisos con Security()

## 📋 Implementación

El sistema de permisos usa `Security()` de FastAPI, lo que proporciona:
- ✅ Validación automática de permisos
- ✅ Documentación en Swagger
- ✅ Integración con el sistema de autenticación existente

## 🔧 Cómo usar

### Importar la función

```python
from fastapi import Security
from core.fastapi.dependencies import require_permissions
```

### Aplicar en un endpoint

```python
@router.get("/users")
async def get_users(
    _: None = Security(require_permissions("users:read"))
):
    return {"users": [...]}
```

### Múltiples permisos (AND)

El usuario debe tener **TODOS** los permisos especificados:

```python
@router.post("/invoices")
async def create_invoice(
    data: InvoiceData,
    _: None = Security(require_permissions("invoices:create", "invoices:write"))
):
    """El usuario DEBE tener ambos permisos"""
    return {"created": True}
```

### Ejemplo completo

```python
from fastapi import APIRouter, Security, Depends
from core.fastapi.dependencies import require_permissions

router = APIRouter(prefix="/invoices", tags=["Invoices"])


@router.get("")
async def list_invoices(
    limit: int = 10,
    _: None = Security(require_permissions("invoices:read"))
):
    """Lista facturas - requiere permiso de lectura"""
    return {"invoices": []}


@router.get("/{invoice_id}")
async def get_invoice(
    invoice_id: int,
    _: None = Security(require_permissions("invoices:read"))
):
    """Obtiene una factura - requiere permiso de lectura"""
    return {"invoice": {...}}


@router.post("")
async def create_invoice(
    data: dict,
    _: None = Security(require_permissions("invoices:create", "invoices:write"))
):
    """Crea una factura - requiere permisos de creación Y escritura"""
    return {"created": True}


@router.put("/{invoice_id}")
async def update_invoice(
    invoice_id: int,
    data: dict,
    _: None = Security(require_permissions("invoices:update", "invoices:write"))
):
    """Actualiza una factura - requiere permisos de actualización Y escritura"""
    return {"updated": True}


@router.delete("/{invoice_id}")
async def delete_invoice(
    invoice_id: int,
    _: None = Security(require_permissions("invoices:delete", "invoices:admin"))
):
    """Elimina una factura - requiere permisos de eliminación Y admin"""
    return {"deleted": True}
```

## 📊 Respuestas HTTP

### 401 Unauthorized - No autenticado
```json
{
  "detail": {
    "error_code": "UNAUTHORIZED",
    "message": "Authentication required for this endpoint",
    "required_permissions": ["users:read"]
  }
}
```

### 403 Forbidden - Sin permisos
```json
{
  "detail": {
    "error_code": "FORBIDDEN",
    "message": "Missing required permissions: users:read",
    "required_permissions": ["users:read", "users:write"],
    "missing_permissions": ["users:read"]
  }
}
```

### 200 OK - Acceso permitido
```json
{
  "users": [...]
}
```

## 🎯 Ventajas de usar Security()

1. **Aparece en Swagger**: Los permisos se muestran en la documentación automática
2. **Candado en Swagger UI**: Muestra un ícono de candado indicando que requiere autenticación
3. **Mejor UX**: El usuario ve claramente qué endpoints requieren permisos
4. **Type safety**: FastAPI valida los tipos automáticamente

## 🔄 Flujo de ejecución

```
Request
  ↓
1. CORSMiddleware (valida CORS)
  ↓
2. AuthenticationMiddleware (valida JWT, carga request.user)
  ↓
3. Routing (FastAPI resuelve el endpoint)
  ↓
4. Security(require_permissions(...)) (valida permisos)
  ↓
5. Endpoint (ejecuta la lógica del negocio)
  ↓
Response
```

## 🧪 Testing

```python
def test_endpoint_with_permission(client, auth_token_with_perms):
    """Usuario con permisos correctos"""
    response = client.get(
        "/users",
        headers={"Authorization": f"Bearer {auth_token_with_perms}"}
    )
    assert response.status_code == 200


def test_endpoint_without_permission(client, auth_token_no_perms):
    """Usuario sin permisos"""
    response = client.get(
        "/users",
        headers={"Authorization": f"Bearer {auth_token_no_perms}"}
    )
    assert response.status_code == 403
    assert response.json()["detail"]["error_code"] == "FORBIDDEN"


def test_endpoint_no_auth(client):
    """Sin autenticación"""
    response = client.get("/users")
    assert response.status_code == 401
    assert response.json()["detail"]["error_code"] == "UNAUTHORIZED"
```

## ⚠️ Notas importantes

1. **Orden del parámetro `_`**: Siempre debe ir **después** de otros `Depends()`:
   ```python
   # ✅ Correcto
   async def endpoint(
       service: MyService = Depends(...),
       _: None = Security(require_permissions(...))
   ):

   # ❌ Incorrecto
   async def endpoint(
       _: None = Security(require_permissions(...)),
       service: MyService = Depends(...)
   ):
   ```

2. **No usar con decoradores**: Ya no necesitas `@require_permissions` como decorador, usa directamente `Security()`.

3. **Autenticación obligatoria**: Si usas `Security(require_permissions(...))`, el endpoint **SIEMPRE** requiere autenticación.

4. **Endpoints públicos**: Si no usas `Security()`, el endpoint será público (sin requerir autenticación).
