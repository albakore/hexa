# Visión General de la Arquitectura

## Introducción

Fast Hexagonal es un proyecto backend construido siguiendo los principios de **Arquitectura Hexagonal** (también conocida como Ports & Adapters), con un enfoque modular y desacoplado.

## Principios de Arquitectura Hexagonal

### ¿Qué es la Arquitectura Hexagonal?

La Arquitectura Hexagonal, propuesta por Alistair Cockburn, separa la lógica de negocio (el "core" de la aplicación) de los detalles de implementación externos (bases de datos, APIs, frameworks).

```
       ┌─────────────────────────────────┐
       │                                 │
  HTTP │   ┌─────────────────────┐       │ Database
 ────► │   │                     │       ├──────►
       │   │    Domain           │       │
       │   │   (Business Logic)  │       │
 Celery│   │                     │       │ Redis
 ────► │   └─────────────────────┘       ├──────►
       │                                 │
       │      Adapters (Ports)           │
       └─────────────────────────────────┘
```

###  Beneficios

1. **Testabilidad**: La lógica de negocio puede testearse sin base de datos o servidor HTTP
2. **Flexibilidad**: Cambiar de FastAPI a otro framework no afecta el dominio
3. **Desacoplamiento**: Los módulos son independientes entre sí
4. **Mantenibilidad**: Cada capa tiene responsabilidades claras

## Capas de la Arquitectura

### 1. Domain (Dominio)

**Ubicación**: `modules/{module}/domain/`

Contiene la lógica de negocio pura, sin dependencias externas.

```python
# modules/invoicing/domain/entity/purchase_invoice.py
from sqlmodel import SQLModel, Field
from datetime import date

class PurchaseInvoice(SQLModel, table=True):
    """Entidad de dominio - Factura de Compra"""
    id: int | None = Field(default=None, primary_key=True)
    number: str
    amount: float
    issue_date: date
    paid: bool = False
```

**Responsabilidades**:
- Definir entidades de negocio
- Reglas de negocio (validaciones, cálculos)
- Value Objects
- Domain Events

**NO debe**:
- Importar FastAPI, SQLAlchemy u otros frameworks
- Hacer queries a base de datos
- Llamar APIs externas

### 2. Ports (Interfaces)

**Ubicación**: `modules/{module}/domain/repository/` y `modules/{module}/domain/usecase/`

Define las interfaces (contracts) que el dominio necesita.

```python
# modules/invoicing/domain/repository/purchase_invoice.py
from abc import ABC, abstractmethod

class PurchaseInvoiceRepository(ABC):
    """Port - Interface del repositorio"""
    
    @abstractmethod
    async def get_purchase_invoice_by_id(self, id: int) -> PurchaseInvoice | None:
        pass
    
    @abstractmethod
    async def save_purchase_invoice(self, invoice: PurchaseInvoice) -> PurchaseInvoice:
        pass
```

**Responsabilidades**:
- Definir contratos que el dominio necesita
- Interfaces de repositorios
- Interfaces de servicios externos

### 3. Use Cases (Casos de Uso)

**Ubicación**: `modules/{module}/domain/usecase/`

Orquesta la lógica de negocio usando entidades y repositorios.

```python
# modules/invoicing/domain/usecase/purchase_invoice.py
class GetPurchaseInvoiceById:
    def __init__(self, repository: PurchaseInvoiceRepository):
        self.repository = repository
    
    async def execute(self, invoice_id: int) -> PurchaseInvoice | None:
        invoice = await self.repository.get_purchase_invoice_by_id(invoice_id)
        
        if not invoice:
            raise InvoiceNotFoundError(f"Invoice {invoice_id} not found")
        
        return invoice
```

**Responsabilidades**:
- Orquestar flujos de negocio
- Coordinar entre entidades y repositorios
- Aplicar reglas de negocio complejas
- Emitir domain events

**NO debe**:
- Conocer detalles de HTTP (request, response)
- Conocer detalles de SQL
- Depender de frameworks

### 4. Adapters (Adaptadores)

Implementaciones concretas de los ports.

#### Adapters de Entrada (Input)

**Ubicación**: `modules/{module}/adapter/input/`

Reciben requests del exterior y los convierten al formato del dominio.

**Tipos**:
- **HTTP/API**: `adapter/input/api/` - Endpoints de FastAPI
- **CLI**: `adapter/input/cli/` - Comandos de terminal
- **Tasks**: `adapter/input/tasks/` - Tareas de Celery
- **Events**: `adapter/input/events/` - Event handlers

```python
# modules/invoicing/adapter/input/api/v1/purchase_invoice.py
from fastapi import APIRouter, Depends

router = APIRouter()

@router.get("/{invoice_id}")
async def get_invoice(
    invoice_id: int,
    service: PurchaseInvoiceService = Depends(get_service)
):
    """Adapter HTTP - Convierte HTTP request a use case"""
    invoice = await service.get_purchase_invoice_by_id(invoice_id)
    return invoice
```

#### Adapters de Salida (Output)

**Ubicación**: `modules/{module}/adapter/output/`

Implementan los ports definidos por el dominio.

**Tipos**:
- **Persistence**: `adapter/output/persistence/` - Repositorios de base de datos
- **API**: `adapter/output/api/` - Clientes HTTP externos
- **Cache**: `adapter/output/cache/` - Redis, Memcached
- **Messaging**: `adapter/output/messaging/` - RabbitMQ, Kafka

```python
# modules/invoicing/adapter/output/persistence/sqlalchemy/purchase_invoice.py
class PurchaseInvoiceSQLAlchemyRepository(PurchaseInvoiceRepository):
    """Adapter de salida - Implementación con SQLAlchemy"""
    
    async def get_purchase_invoice_by_id(self, id: int):
        query = select(PurchaseInvoice).where(PurchaseInvoice.id == id)
        result = await global_session.execute(query)
        return result.scalars().first()
```

### 5. Application Services

**Ubicación**: `modules/{module}/application/service/`

Capa intermedia que coordina use cases y puede agregar funcionalidad transversal.

```python
# modules/invoicing/application/service/purchase_invoice.py
class PurchaseInvoiceService:
    def __init__(self, repository: PurchaseInvoiceRepository):
        self.repository = repository
        self.usecase_factory = InvoiceUseCaseFactory(repository)
    
    async def get_purchase_invoice_by_id(self, id: int) -> PurchaseInvoice:
        """Service - Agrega logging, validación, etc."""
        usecase = self.usecase_factory.get_purchase_invoice_by_id()
        return await usecase.execute(id)
```

**Responsabilidades**:
- Coordinar múltiples use cases
- Agregar concerns transversales (logging, caching)
- Transacciones
- Validación de permisos

## Flujo de una Request

```
1. HTTP Request
   ↓
2. FastAPI Router (Input Adapter)
   ↓
3. Application Service
   ↓
4. Use Case
   ↓
5. Domain Entity + Repository (Port)
   ↓
6. Repository Adapter (Output Adapter)
   ↓
7. Database
```

### Ejemplo Completo

```python
# 1. Request HTTP
GET /api/invoicing/v1/purchase_invoice/123

# 2. Input Adapter (API)
@router.get("/{invoice_id}")
async def get_invoice(invoice_id: int, service: PurchaseInvoiceService):
    return await service.get_purchase_invoice_by_id(invoice_id)

# 3. Application Service
async def get_purchase_invoice_by_id(self, id: int):
    usecase = self.usecase_factory.get_purchase_invoice_by_id()
    return await usecase.execute(id)

# 4. Use Case
async def execute(self, invoice_id: int):
    invoice = await self.repository.get_purchase_invoice_by_id(invoice_id)
    if not invoice:
        raise InvoiceNotFoundError()
    return invoice

# 5. Repository (Port - Interface)
@abstractmethod
async def get_purchase_invoice_by_id(self, id: int) -> PurchaseInvoice | None:
    pass

# 6. Repository Adapter (SQLAlchemy)
async def get_purchase_invoice_by_id(self, id: int):
    query = select(PurchaseInvoice).where(PurchaseInvoice.id == id)
    result = await global_session.execute(query)
    return result.scalars().first()

# 7. Database Query
SELECT * FROM purchaseinvoice WHERE id = 123
```

## Arquitectura Modular

Cada módulo es una "mini-aplicación" hexagonal independiente:

```
modules/invoicing/
├── domain/              # Lógica de negocio pura
│   ├── entity/         # Entidades
│   ├── repository/     # Interfaces (ports)
│   └── usecase/        # Casos de uso
├── application/         # Servicios de aplicación
│   └── service/
├── adapter/            # Adaptadores
│   ├── input/          # Entrada (API, Tasks)
│   └── output/         # Salida (DB, APIs externas)
├── container.py        # Dependency Injection
└── module.py          # Registro del módulo
```

## Comunicación Entre Módulos

Los módulos NO deben importarse directamente entre sí. Se usa **Service Locator**:

```python
# ❌ MAL - Acoplamiento directo
from modules.user.application.service.user import UserService

# ✅ BIEN - Desacoplado
user_service = service_locator.get_service("user_service")
```

Ver más en [Service Locator Pattern](./04-service-locator.md).

## Ventajas de Esta Arquitectura

1. **Módulos Independientes**: Cada módulo puede desarrollarse, testearse y desplegarse de forma independiente
2. **Testeable**: Lógica de negocio sin dependencias de infraestructura
3. **Flexible**: Cambiar implementaciones sin afectar el dominio
4. **Escalable**: Fácil agregar nuevos módulos
5. **Mantenible**: Responsabilidades claras en cada capa

## Siguiente Paso

Lee [Estructura del Proyecto](./02-project-structure.md) para entender la organización de carpetas.
