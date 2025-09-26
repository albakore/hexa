# API Reference

## Información General

### Base URL
```
http://localhost:8000
```

### Comando de Ejecución
```bash
# Desarrollo
uv run hexa dev

# Producción
gunicorn core.fastapi.server:app -w 4 -k uvicorn.workers.UvicornWorker
```

### Autenticación
La API utiliza JWT Bearer tokens para autenticación:
```
Authorization: Bearer <token>
```

### Formato de Respuesta
Todas las respuestas están en formato JSON:
```json
{
  "data": {},
  "message": "Success",
  "status": 200
}
```

### Códigos de Estado HTTP
- `200` - OK
- `201` - Created
- `204` - No Content
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `409` - Conflict
- `422` - Validation Error
- `500` - Internal Server Error

## Endpoints de Sistema

### Health Check
```http
GET /health
```

**Respuesta:**
```json
{
  "status": "healthy",
  "message": "Minimal version running successfully",
  "architecture": "hexagonal_decoupled_minimal"
}
```

### Módulos Activos
```http
GET /modules
```

**Respuesta:**
```json
{
  "message": "All modules active and loaded",
  "active_modules": [
    "auth", "users", "rbac", "finance", 
    "providers", "user-relationships", "yiqi-erp", "modules"
  ],
  "total_routes": 9
}
```

### Permisos del Sistema
```http
GET /permissions
```

**Respuesta:**
```json
{
  "taxes": [
    {"token": "taxes:read", "description": "Lee Impuestos"},
    {"token": "taxes:write", "description": "Crea Impuestos"}
  ],
  "providers": [
    {"token": "providers:read", "description": "Lee proveedores"},
    {"token": "providers:invoices_read", "description": "Visualiza las facturas del proveedor"}
  ]
}
```

### Documentación Interactiva
```http
GET /docs
```
Swagger UI con documentación interactiva de la API.

```http
GET /redoc
```
ReDoc con documentación alternativa de la API.

## Módulo de Autenticación

**Base Path:** `/api/v1/auth`

### Login
```http
POST /api/v1/auth/login
```

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

### Refresh Token
```http
POST /api/v1/auth/refresh
```

**Request Body:**
```json
{
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### Verificar Token
```http
POST /api/v1/auth/verify
```

### Registro
```http
POST /api/v1/auth/register
```

### Reset de Contraseña
```http
POST /api/v1/auth/password_reset
```

**Headers:**
```
Authorization: Bearer <token>
```

## Módulo de Usuarios

**Base Path:** `/api/v1/users`

### Crear Usuario
```http
POST /api/v1/users
```

**Request Body:**
```json
{
  "email": "newuser@example.com",
  "password": "securepassword123"
}
```

**Response:**
```json
{
  "id": 1,
  "email": "newuser@example.com",
  "is_active": true,
  "created_at": "2024-01-01T00:00:00Z"
}
```

### Listar Usuarios
```http
GET /api/v1/users?limit=10&page=0
```

**Query Parameters:**
- `page` (int, optional): Número de página (default: 1)
- `size` (int, optional): Tamaño de página (default: 10)
- `search` (string, optional): Buscar por email

**Response:**
```json
{
  "items": [
    {
      "id": 1,
      "email": "user@example.com",
      "is_active": true,
      "created_at": "2024-01-01T00:00:00Z"
    }
  ],
  "total": 1,
  "page": 1,
  "size": 10,
  "pages": 1
}
```

### Buscar Usuarios
```http
GET /api/v1/users/search?token_modules[]=auth&token_modules[]=rbac
```

### Obtener Usuario
```http
GET /api/v1/users/{user_uuid}
```

**Response:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "is_active": true,
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

### Asignar Rol a Usuario
```http
PUT /api/v1/users/{user_uuid}/role
```

**Request Body:**
```json
{
  "email": "updated@example.com"
}
```

**Request Body:**
```json
{
  "id": 1
}
```

## Módulo RBAC

**Base Path:** `/api/v1/rbac`

### Listar Roles
```http
GET /api/v1/rbac/role
```

**Request Body:**
```json
{
  "name": "admin",
  "description": "Administrator role"
}
```

**Response:**
```json
{
  "id": 1,
  "name": "admin",
  "description": "Administrator role",
  "is_active": true,
  "created_at": "2024-01-01T00:00:00Z",
  "permissions": []
}
```

### Listar Permisos
```http
GET /api/v1/rbac/permission
```

**Request Body:**
```json
{
  "name": "user:create",
  "resource": "user",
  "action": "create",
  "description": "Create users"
}
```

### Health Check RBAC
```http
GET /api/v1/rbac/health
```

**Response:**
```json
{
  "user_id": 1,
  "roles": [
    {
      "id": 1,
      "name": "admin",
      "description": "Administrator role",
      "permissions": [
        {
          "id": 1,
          "name": "user:create",
          "resource": "user",
          "action": "create"
        }
      ]
    }
  ]
}
```

### Verificar Permiso
```http
POST /rbac/permissions/check
```

**Request Body:**
```json
{
  "user_id": 1,
  "resource": "user",
  "action": "create"
}
```

**Response:**
```json
{
  "has_permission": true,
  "user_id": 1,
  "resource": "user",
  "action": "create"
}
```

## Módulo de Finanzas

**Base Path:** `/api/v1/finance/currencies`

### Crear Moneda
```http
POST /api/v1/finance/currencies
```

**Request Body:**
```json
{
  "code": "USD",
  "name": "US Dollar",
  "symbol": "$"
}
```

### Listar Monedas
```http
GET /api/v1/finance/currencies
```

### Obtener Moneda
```http
GET /api/v1/finance/currencies/{id_currency}
```

### Actualizar Moneda
```http
PUT /api/v1/finance/currencies
```

### Eliminar Moneda
```http
DELETE /api/v1/finance/currencies/{id_currency}
```

**Response:**
```json
[
  {
    "id": 1,
    "code": "USD",
    "name": "US Dollar",
    "symbol": "$",
    "is_active": true,
    "exchange_rate": "1.0"
  }
]
```

### Convertir Moneda
```http
POST /finance/convert
```

**Request Body:**
```json
{
  "amount": "100.00",
  "from_currency": "USD",
  "to_currency": "EUR"
}
```

**Response:**
```json
{
  "original_amount": "100.00",
  "original_currency": "USD",
  "converted_amount": "85.50",
  "target_currency": "EUR",
  "exchange_rate": "0.855",
  "conversion_date": "2024-01-01T00:00:00Z"
}
```

## Módulo de Proveedores

**Base Path:** `/api/v1/providers`

### Crear Proveedor
```http
POST /api/v1/providers
```

**Request Body:**
```json
{
  "name": "Acme Corp",
  "tax_id": "12345678901",
  "email": "contact@acme.com"
}
```

### Listar Proveedores
```http
GET /api/v1/providers?limit=10&page=0
```

### Obtener Proveedor
```http
GET /api/v1/providers/{id_provider}
```

### Actualizar Proveedor
```http
PUT /api/v1/providers
```

### Eliminar Proveedor
```http
DELETE /api/v1/providers/{id_provider}
```

## Facturas Borrador de Proveedores

**Base Path:** `/api/v1/providers/draft-invoices`

### Listar Facturas Borrador
```http
GET /api/v1/providers/draft-invoices?id_provider=1&limit=10&page=0
```

### Obtener Factura Borrador
```http
GET /api/v1/providers/draft-invoices/{id_draft_invoice}
```

### Crear Factura Borrador
```http
POST /api/v1/providers/draft-invoices
```

### Actualizar Factura Borrador
```http
PUT /api/v1/providers/draft-invoices/{id_draft_invoice}
```

### Eliminar Factura Borrador
```http
DELETE /api/v1/providers/draft-invoices/{id_draft_invoice}
```

### Emitir Factura
```http
POST /api/v1/providers/draft-invoices/{id_draft_invoice}/emit
```

**Request Body:**
```json
{
  "total_amount": "1000.00",
  "currency": "USD",
  "items": [
    {
      "description": "Service A",
      "quantity": 1,
      "unit_price": "1000.00"
    }
  ]
}
```

## Módulo YiQi ERP

**Base Path:** `/api/v1/yiqi-erp`

### Listar Monedas YiQi
```http
GET /api/v1/yiqi-erp/currency_list?id_schema=1
```

### Obtener Moneda por Código
```http
GET /api/v1/yiqi-erp/currency_list/{currency_code}?id_schema=1
```

### Listar Servicios
```http
GET /api/v1/yiqi-erp/services_list?id_schema=1
```

### Obtener Proveedor YiQi
```http
GET /api/v1/yiqi-erp/provider/{id_provider}?id_schema=1
```

### Subir Archivo
```http
POST /api/v1/yiqi-erp/upload_file
```

**Response:**
```json
{
  "synced_companies": 5,
  "new_companies": 2,
  "updated_companies": 3,
  "sync_timestamp": "2024-01-01T00:00:00Z"
}
```

## Relaciones de Usuario

**Base Path:** `/api/v1/user-relationships`

### Obtener Instancia de Entidad
```http
GET /api/v1/user-relationships/entity?entity_key=provider&entity_id=1
```

### Obtener Relaciones de Usuario
```http
GET /api/v1/user-relationships/{user_uuid}?entity_key=provider
```

### Asociar Usuario con Entidad
```http
POST /api/v1/user-relationships/{user_uuid}/link?entity_key=provider&entity_id=1
```

### Eliminar Asociación
```http
DELETE /api/v1/user-relationships/{user_uuid}/link?entity_key=provider&entity_id=1
```

**Request Body:**
```json
{
  "empresa_id": 1,
  "numero": "F001-00000001",
  "total": "1000.00",
  "moneda": "USD",
  "items": [
    {
      "descripcion": "Producto A",
      "cantidad": 1,
      "precio_unitario": "1000.00"
    }
  ]
}
```

## Información de Módulos

**Base Path:** `/api/v1/modules`

### Listar Módulos del Sistema
```http
GET /api/v1/modules
```

## Almacenamiento de Archivos

**Base Path:** `/api/v1/filestorage`

### Subir Archivo
```http
POST /api/v1/filestorage/v1/filestorage/upload
```

**Request (multipart/form-data):**
```
file: <binary_file>
description: "Document description"
```

**Response:**
```json
{
  "file_id": "uuid-here",
  "filename": "document.pdf",
  "size": 1024000,
  "content_type": "application/pdf",
  "upload_date": "2024-01-01T00:00:00Z",
  "url": "/file-storage/files/uuid-here"
}
```

### Descargar Archivo
```http
POST /api/v1/filestorage/v1/filestorage/{uuid_file}/download
```

### Obtener Información de Archivo
```http
GET /api/v1/filestorage/v1/filestorage/{uuid_file}
```

## Códigos de Error Comunes

### Error de Validación (422)
```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

### Error de Autenticación (401)
```json
{
  "detail": "Could not validate credentials"
}
```

### Error de Permisos (403)
```json
{
  "detail": "Permission required: user:create"
}
```

### Error de Recurso No Encontrado (404)
```json
{
  "detail": "User not found"
}
```

### Error de Conflicto (409)
```json
{
  "detail": "User with email already exists"
}
```

## Rate Limiting

La API implementa rate limiting por usuario:
- **Límite**: 60 requests por minuto
- **Header de respuesta**: `X-RateLimit-Remaining`
- **Error**: 429 Too Many Requests

## Paginación

Los endpoints que retornan listas soportan paginación:

**Query Parameters:**
- `page`: Número de página (empezando en 1)
- `size`: Número de elementos por página (máximo 100)

**Response Headers:**
- `X-Total-Count`: Total de elementos
- `X-Page-Count`: Total de páginas

## Filtrado y Búsqueda

Muchos endpoints soportan filtrado:

**Query Parameters comunes:**
- `search`: Búsqueda de texto
- `active`: Filtrar por estado activo (true/false)
- `created_after`: Filtrar por fecha de creación
- `created_before`: Filtrar por fecha de creación

## Webhooks

El sistema puede enviar webhooks para eventos importantes:

### Configurar Webhook
```http
POST /webhooks
```

**Request Body:**
```json
{
  "url": "https://your-app.com/webhook",
  "events": ["user.created", "user.updated"],
  "secret": "webhook-secret"
}
```

### Eventos Disponibles
- `user.created`
- `user.updated`
- `user.deleted`
- `provider.created`
- `invoice.created`
- `payment.processed`

## SDKs y Librerías

### Python SDK
```python
from fast_hexagonal_client import Client

client = Client(
    base_url="http://localhost:8000",
    token="your-jwt-token"
)

# Crear usuario
user = client.users.create(
    email="test@example.com",
    password="password123"
)
```

### JavaScript SDK
```javascript
import { FastHexagonalClient } from 'fast-hexagonal-client';

const client = new FastHexagonalClient({
  baseUrl: 'http://localhost:8000',
  token: 'your-jwt-token'
});

// Crear usuario
const user = await client.users.create({
  email: 'test@example.com',
  password: 'password123'
});
```

## Ejemplos de Uso

### Flujo Completo de Autenticación
```bash
# 1. Login
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@example.com", "password": "admin123"}'

# 2. Usar token en requests
curl -X GET http://localhost:8000/users \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
```

### Crear Usuario con Rol
```bash
# 1. Crear usuario
USER_RESPONSE=$(curl -X POST http://localhost:8000/users \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"email": "newuser@example.com", "password": "password123"}')

USER_ID=$(echo $USER_RESPONSE | jq -r '.id')

# 2. Asignar rol
curl -X POST http://localhost:8000/rbac/users/$USER_ID/roles/1 \
  -H "Authorization: Bearer $TOKEN"
```

## Monitoreo y Métricas

### Métricas de Sistema
```http
GET /metrics
```

Retorna métricas en formato Prometheus.

### Health Checks Detallados
```http
GET /health/detailed
```

**Response:**
```json
{
  "status": "healthy",
  "checks": {
    "database": "ok",
    "redis": "ok",
    "external_apis": "ok"
  },
  "modules": {
    "auth": {"status": "healthy", "version": "1.0.0"},
    "user": {"status": "healthy", "version": "1.2.0"}
  }
}
```