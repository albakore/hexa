# Fix para Tests de Repositorio

## Problema Identificado

Los tests de repositorio estaban instanciando los adapters sin inyectar las dependencias necesarias:

```python
# ❌ INCORRECTO
repository = PurchaseInvoiceRepositoryAdapter()  # Sin dependencias
```

Los adapters son **wrappers** que requieren que se les inyecte el repositorio real:

```python
@dataclass
class PurchaseInvoiceRepositoryAdapter(PurchaseInvoiceRepository):
    repository: PurchaseInvoiceRepository  # ← Requiere inyección
```

## Solución Implementada

### 1. Fixture en `conftest.py` del módulo

Se creó una fixture que inyecta correctamente las dependencias:

```python
@pytest.fixture
def real_purchase_invoice_repository(db_session) -> PurchaseInvoiceRepositoryAdapter:
    """
    Repositorio real conectado a la base de datos de test.
    """
    from modules.invoicing.adapter.output.persistence.sqlalchemy.purchase_invoice import (
        PurchaseInvoiceSQLAlchemyRepository,
    )

    # Inyectar el repositorio SQLAlchemy real
    sqlalchemy_repo = PurchaseInvoiceSQLAlchemyRepository()
    return PurchaseInvoiceRepositoryAdapter(repository=sqlalchemy_repo)
```

### 2. Actualizar Tests para usar la Fixture

```python
async def test_save_purchase_invoice(
    self,
    db_session,
    real_purchase_invoice_repository: PurchaseInvoiceRepositoryAdapter,  # ← Usar fixture
    sample_purchase_invoice: PurchaseInvoice,
):
    # Usar la fixture en lugar de instanciar manualmente
    saved_invoice = await real_purchase_invoice_repository.save_purchase_invoice(sample_purchase_invoice)
    assert saved_invoice.id is not None
```

## Problema Secundario: Transacciones en Tests

### Síntoma

Los tests que guardan y luego consultan (`save` → `get`) fallan con `assert None is not None`:

```python
async def test_get_purchase_invoice_by_id(
    self,
    db_session,
    real_purchase_invoice_repository,
    sample_purchase_invoice,
):
    # Guardar
    saved_invoice = await repository.save_purchase_invoice(sample_purchase_invoice)
    invoice_id = saved_invoice.id

    # Consultar (FALLA - retorna None)
    retrieved_invoice = await repository.get_purchase_invoice_by_id(invoice_id)
    assert retrieved_invoice is not None  # ❌ Falla aquí
```

### Causa

El repositorio SQLAlchemy usa `flush()` en lugar de `commit()`:

```python
async def save_purchase_invoice(self, purchase_invoice: PurchaseInvoice):
    global_session.add(purchase_invoice)
    await global_session.flush()  # ← Solo flush, no commit
    return purchase_invoice
```

`flush()` envía los cambios a la base de datos pero **NO** hace commit de la transacción. Los objetos flusheados no son visibles para consultas posteriores en la misma sesión sin hacer un refresh explícito.

### Soluciones Posibles

#### Opción 1: Commit explícito en el repositorio (NO RECOMENDADO)

Cambiar `flush()` por `commit()` en `save_purchase_invoice`:

```python
async def save_purchase_invoice(self, purchase_invoice: PurchaseInvoice):
    global_session.add(purchase_invoice)
    await global_session.commit()  # Commit en lugar de flush
    return purchase_invoice
```

**Problema**: Esto rompe el patrón de Unit of Work y hace commits prematuros.

#### Opción 2: Usar el Container en los tests (RECOMENDADO)

En lugar de crear fixtures personalizadas, usar directamente el container del módulo:

```python
@pytest.fixture
def purchase_invoice_repository(db_session):
    """Usa el container para obtener el repositorio con todas las dependencias."""
    from modules.invoicing.container import InvoicingContainer
    container = InvoicingContainer()
    return container.purchase_invoice_adapter()
```

#### Opción 3: Hacer commit en los tests

Agregar `await db_session.commit()` después de cada operación de escritura:

```python
async def test_get_purchase_invoice_by_id(
    self,
    db_session,
    real_purchase_invoice_repository,
    sample_purchase_invoice,
):
    saved_invoice = await repository.save_purchase_invoice(sample_purchase_invoice)
    await db_session.commit()  # ← Commit explícito en el test
    invoice_id = saved_invoice.id

    retrieved_invoice = await repository.get_purchase_invoice_by_id(invoice_id)
    assert retrieved_invoice is not None  # ✅ Ahora funciona
```

**Problema**: El `db_session` del test puede NO ser el mismo que `global_session` del repositorio.

#### Opción 4: Refrescar la sesión después de flush

```python
async def save_purchase_invoice(self, purchase_invoice: PurchaseInvoice):
    global_session.add(purchase_invoice)
    await global_session.flush()
    await global_session.refresh(purchase_invoice)  # ← Refresh después de flush
    return purchase_invoice
```

## Pasos para Aplicar el Fix a Todos los Módulos

### 1. Actualizar `conftest.py` de cada módulo

Para cada módulo que tenga repositorios, actualizar su `test/conftest.py`:

```python
@pytest.fixture
def real_{module}_repository(db_session):
    from modules.{module}.adapter.output.persistence.sqlalchemy.{entity} import (
        {Entity}SQLAlchemyRepository,
    )
    from modules.{module}.adapter.output.persistence.{entity}_adapter import (
        {Entity}RepositoryAdapter,
    )

    sqlalchemy_repo = {Entity}SQLAlchemyRepository()
    return {Entity}RepositoryAdapter(repository=sqlalchemy_repo)
```

### 2. Actualizar todos los tests de repositorio

Buscar y reemplazar en todos los archivos `test_*_repository.py`:

```bash
# Buscar
repository = {SomeAdapter}()

# Reemplazar por
repository = real_{module}_repository
```

Y agregar el parámetro a la firma del método:

```python
async def test_method(
    self,
    db_session,
    real_{module}_repository: {ModuleAdapter},  # ← Agregar
    ...
):
```

### 3. Módulos Afectados

- ✅ `modules/invoicing` - Ya corregido
- ⏳ `modules/auth`
- ⏳ `modules/finance`
- ⏳ `modules/notifications`
- ⏳ `modules/provider`
- ⏳ `modules/rbac`
- ⏳ `modules/user`

## Comando para Ejecutar Tests

```bash
# Test de un módulo específico
pytest modules/invoicing/test/test_purchase_invoice_repository.py -v

# Todos los tests de repositorio
pytest -k "repository" -v

# Solo tests de integración
pytest -m integration -v
```

## Conclusión

El problema principal era la **falta de inyección de dependencias** en los tests. La solución es crear fixtures que inyecten correctamente las dependencias usando el mismo patrón que usan los containers en producción.

El problema secundario de transacciones requiere análisis adicional del flujo de sesiones en el sistema.
