# Mixins para Modelos SQLModel

Este módulo proporciona mixins reutilizables que agregan funcionalidad común a los modelos de la aplicación.

## Mixins Disponibles

### 1. TimestampMixin

Agrega campos de timestamp que se actualizan automáticamente.

**Campos agregados:**
- `created_at`: Fecha y hora de creación del registro (se establece automáticamente)
- `updated_at`: Fecha y hora de última modificación (se actualiza automáticamente en cada cambio)

**Uso:**

```python
from sqlmodel import SQLModel, Field
from shared.mixins import TimestampMixin

class Provider(TimestampMixin, SQLModel, table=True):
    id: int | None = Field(None, primary_key=True)
    name: str
    # ... otros campos
```

**Características:**
- ✅ `created_at` se establece automáticamente al crear el registro
- ✅ `updated_at` se actualiza automáticamente cada vez que se modifica el registro
- ✅ Usa `server_default=func.now()` para valores por defecto en la base de datos
- ✅ Compatible con timezone-aware timestamps

### 2. UserTimestampMixin

Mixin especializado para modelos de usuario que incluye campos de sesión además de timestamps.

**Campos agregados:**
- `date_registration`: Fecha de registro del usuario (auto)
- `date_last_session`: Fecha de última sesión (nullable, debe actualizarse manualmente)
- `created_at`: Fecha y hora de creación del registro (auto)
- `updated_at`: Fecha y hora de última modificación (auto)

**Uso:**

```python
from sqlmodel import SQLModel, Field
import uuid
from shared.mixins import UserTimestampMixin

class User(UserTimestampMixin, SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    email: str
    password: str
    # ... otros campos
```

**Actualizar última sesión:**

```python
# En el servicio de autenticación
async def update_last_session(user: User):
    from datetime import datetime
    user.date_last_session = datetime.now()
    await repository.save(user)
```

### 3. SoftDeleteMixin

Agrega funcionalidad de "soft delete" (borrado lógico) a los modelos.

**Campos agregados:**
- `deleted_at`: Fecha y hora de eliminación (null si no está eliminado)
- `is_deleted`: Bandera booleana que indica si está eliminado

**Uso:**

```python
from sqlmodel import SQLModel, Field
from shared.mixins import SoftDeleteMixin, TimestampMixin

class Document(SoftDeleteMixin, TimestampMixin, SQLModel, table=True):
    id: int | None = Field(None, primary_key=True)
    title: str
    content: str
```

**Implementar soft delete:**

```python
from datetime import datetime

# Marcar como eliminado
async def soft_delete(document: Document):
    document.is_deleted = True
    document.deleted_at = datetime.now()
    await repository.save(document)

# Restaurar
async def restore(document: Document):
    document.is_deleted = False
    document.deleted_at = None
    await repository.save(document)

# Filtrar registros no eliminados
async def get_active_documents():
    query = select(Document).where(Document.is_deleted == False)
    # ...
```

## Modelos Actualizados

Los siguientes modelos ya están usando los mixins:

### Con TimestampMixin
- ✅ `Provider` - Proveedores
- ✅ `PurchaseInvoice` - Facturas de compra
- ✅ `DraftPurchaseInvoice` - Borradores de facturas
- ✅ `PurchaseInvoiceService` - Servicios de factura

### Con UserTimestampMixin
- ✅ `User` - Usuarios del sistema

## Cómo Agregar Timestamps a un Modelo Nuevo

1. Importa el mixin apropiado:

```python
from shared.mixins import TimestampMixin
```

2. Agrega el mixin como clase base (ANTES de SQLModel):

```python
class MyNewModel(TimestampMixin, SQLModel, table=True):
    # ... campos del modelo
```

3. No necesitas definir `created_at` ni `updated_at` - el mixin los agrega automáticamente

## Actualización Automática

### created_at
- Se establece automáticamente cuando se inserta un nuevo registro
- Usa `server_default=func.now()` (se ejecuta en la base de datos)
- No se puede modificar después de la creación

### updated_at
- Se establece automáticamente en la creación
- Se actualiza automáticamente cada vez que se modifica el registro
- Usa `onupdate=func.now()` (se ejecuta en la base de datos al actualizar)

### date_last_session (User)
- Debe actualizarse manualmente en el código de autenticación
- Es nullable para permitir usuarios que nunca han iniciado sesión

## Combinando Mixins

Puedes combinar múltiples mixins en un modelo:

```python
class ImportantDocument(SoftDeleteMixin, TimestampMixin, SQLModel, table=True):
    id: int | None = Field(None, primary_key=True)
    title: str
    content: str
```

**Orden de herencia recomendado:**
1. Mixins específicos (SoftDeleteMixin, UserTimestampMixin)
2. Mixins generales (TimestampMixin)
3. SQLModel
4. table=True

## Migraciones de Base de Datos

Después de agregar mixins a modelos existentes, necesitas crear y aplicar migraciones:

```bash
# Crear migración
alembic revision --autogenerate -m "Add timestamps to models"

# Aplicar migración
alembic upgrade head
```

## Notas Técnicas

- Los mixins usan `@declared_attr` de SQLAlchemy para agregar campos dinámicamente
- Los campos usan `sa_column=Column(...)` para tener control completo sobre la definición de la columna
- `func.now()` se ejecuta en el servidor de base de datos, no en Python
- Los timestamps son timezone-aware (`DateTime(timezone=True)`)

## Mejores Prácticas

1. **Siempre usa TimestampMixin** para tablas que representen datos de negocio
2. **Usa UserTimestampMixin** solo para modelos de usuario/autenticación
3. **Usa SoftDeleteMixin** para datos que necesitan auditoría de eliminación
4. **No modifiques manualmente** `created_at` o `updated_at`
5. **Actualiza `date_last_session`** en cada inicio de sesión exitoso
6. **Implementa filtros** para excluir registros eliminados cuando uses SoftDeleteMixin

## Ejemplo Completo

```python
from datetime import date
from sqlmodel import SQLModel, Field
from shared.mixins import TimestampMixin

class Invoice(TimestampMixin, SQLModel, table=True):
    """
    Modelo de factura con timestamps automáticos.

    created_at y updated_at se manejan automáticamente.
    """
    id: int | None = Field(None, primary_key=True)
    number: str
    amount: float
    issue_date: date
    fk_provider: int

# Uso en repositorio
async def create_invoice(data: dict):
    invoice = Invoice(**data)
    # created_at se establece automáticamente
    await session.add(invoice)
    await session.commit()
    return invoice

async def update_invoice(invoice: Invoice, data: dict):
    for key, value in data.items():
        setattr(invoice, key, value)
    # updated_at se actualiza automáticamente
    await session.commit()
    return invoice
```
