# Módulo de Búsqueda Dinámica

Este módulo proporciona funcionalidad reutilizable para implementar búsquedas dinámicas con filtros en repositorios SQLAlchemy.

## Características

- 🔍 Búsqueda dinámica con múltiples operadores
- 📊 Soporte para paginación
- 📅 Conversión automática de fechas
- 🎯 Validación de campos y operadores
- ♻️ Código reutilizable para todos los repositorios

## Operadores Soportados

- `eq` - Igual a
- `ne` - No igual a / Distinto de
- `gt` - Mayor que
- `gte` - Mayor o igual que
- `lt` - Menor que
- `lte` - Menor o igual que
- `contains` - Contiene (para strings)
- `not_contains` - No contiene
- `between` - Entre dos valores (requiere `value` y `value2`)
- `in` - Está en una lista de valores
- `not_in` - No está en una lista de valores
- `is_null` - Es nulo
- `is_not_null` - No es nulo

## Uso

### 1. Heredar de DynamicSearchMixin en tu repositorio

```python
from core.search import DynamicSearchMixin
from sqlalchemy import AsyncSession

class MyRepository(DynamicSearchMixin):
    # Definir la clase del modelo
    model_class = MyModel

    # Definir campos de fecha (opcional)
    date_fields = {
        "created_at",
        "updated_at",
        "start_date",
    }

    async def search(self, filters, limit, page):
        async with session_factory() as session:
            return await self.dynamic_search(
                session=session,
                filters=filters,
                limit=limit,
                page=page
            )
```

### 2. Crear comandos de búsqueda

```python
from core.search import FilterCriteria, FilterOperator
from pydantic import BaseModel, Field
from typing import List

class SearchMyModelCommand(BaseModel):
    filters: List[FilterCriteria] = Field(
        default=[], description="Lista de filtros a aplicar"
    )
    limit: int = Field(default=20, ge=1, le=50000)
    page: int = Field(default=0, ge=0)
```

### 3. Usar en tu aplicación

```python
# Crear filtros
filters = [
    FilterCriteria(
        field="name",
        operator=FilterOperator.CONTAINS,
        value="john"
    ),
    FilterCriteria(
        field="age",
        operator=FilterOperator.GREATER_THAN,
        value=18
    ),
    FilterCriteria(
        field="created_at",
        operator=FilterOperator.BETWEEN,
        value="2025-01-01",
        value2="2025-12-31"
    )
]

# Ejecutar búsqueda
command = SearchMyModelCommand(filters=filters, limit=20, page=0)
items, total = await repository.search(command.filters, command.limit, command.page)
```

## Ejemplos de Uso en el Proyecto

### PurchaseInvoiceSQLAlchemyRepository

```python
from core.search import DynamicSearchMixin

class PurchaseInvoiceSQLAlchemyRepository(DynamicSearchMixin, PurchaseInvoiceRepository):
    model_class = PurchaseInvoice
    date_fields = {
        "service_month",
        "issue_date",
        "receipt_date",
        "period_from_date",
        "period_until_date",
    }

    async def search_purchase_invoices(
        self, command: SearchPurchaseInvoiceCommand
    ) -> tuple[List[PurchaseInvoice] | Sequence[PurchaseInvoice], int]:
        async with session_factory() as session:
            return await self.dynamic_search(
                session=session,
                filters=command.filters,
                limit=command.limit,
                page=command.page
            )
```

### DraftPurchaseInvoiceSQLAlchemyRepository

```python
from core.search import DynamicSearchMixin

class DraftPurchaseInvoiceSQLAlchemyRepository(DynamicSearchMixin, DraftPurchaseInvoiceRepository):
    model_class = DraftPurchaseInvoice
    date_fields = {"service_month", "issue_date", "receipt_date"}

    async def search_draft_invoices(
        self, command: SearchDraftPurchaseInvoiceCommand
    ) -> tuple[List[DraftPurchaseInvoice] | Sequence[DraftPurchaseInvoice], int]:
        async with session_factory() as session:
            return await self.dynamic_search(
                session=session,
                filters=command.filters,
                limit=command.limit,
                page=command.page
            )
```

## Formato de Fechas

Los campos definidos en `date_fields` aceptan strings en formato `YYYY-MM-DD` y se convierten automáticamente a objetos `date`.

```python
FilterCriteria(
    field="issue_date",
    operator=FilterOperator.GREATER_THAN_OR_EQUAL,
    value="2025-01-01"  # Se convierte automáticamente a date
)
```

## Manejo de Errores

El mixin lanza `ValueError` en los siguientes casos:

- Campo no existe en el modelo
- Operador no soportado
- Formato de fecha inválido
- Falta `value2` para operador `between`
- Valor no es una lista para operadores `in` o `not_in`

## Ventajas

✅ **DRY (Don't Repeat Yourself)**: Elimina código duplicado entre repositorios
✅ **Mantenibilidad**: Los cambios se hacen en un solo lugar
✅ **Consistencia**: Todos los repositorios usan la misma lógica de filtrado
✅ **Extensibilidad**: Fácil agregar nuevos operadores o funcionalidad
✅ **Type Safety**: Usa Pydantic para validación de tipos
