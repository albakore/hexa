# Guía de Testing

## Introducción

Este proyecto utiliza **pytest** como framework de testing con soporte para tests asíncronos mediante **pytest-asyncio**.

La estrategia de testing sigue la arquitectura hexagonal del proyecto, con tests para cada capa:
- **Repositorios** (Adapters de salida - Integración con DB)
- **Casos de Uso** (Domain - Lógica de negocio)
- **Servicios** (Application - Coordinación)
- **Tasks** (Adapters de entrada - Celery)

---

## Estructura de Tests

```
backend/
├── conftest.py                          # Fixtures globales compartidos
├── pytest.ini                           # Configuración de pytest (en pyproject.toml)
└── modules/
    └── {module_name}/
        └── test/
            ├── __init__.py
            ├── conftest.py              # Fixtures específicos del módulo
            ├── test_{entity}_repository.py   # Tests de integración (DB)
            ├── test_{entity}_usecase.py      # Tests unitarios (mocks)
            ├── test_{entity}_service.py      # Tests unitarios + integración
            └── test_tasks.py                 # Tests de Celery tasks
```

---

## Tipos de Tests

### 1. Tests Unitarios (`@pytest.mark.unit`)

**Características:**
- Usan mocks para dependencias
- No acceden a base de datos
- Rápidos de ejecutar
- Prueban lógica aislada

**Ejemplo:**
```python
@pytest.mark.unit
@pytest.mark.asyncio
async def test_get_invoice_by_id(
    mock_purchase_invoice_repository: AsyncMock,
    sample_purchase_invoice_with_id: PurchaseInvoice,
):
    # Arrange
    mock_purchase_invoice_repository.get_purchase_invoice_by_id.return_value = sample_purchase_invoice_with_id
    usecase = GetPurchaseInvoiceById(mock_purchase_invoice_repository)

    # Act
    result = await usecase(id_purchase_invoice=123)

    # Assert
    assert result == sample_purchase_invoice_with_id
```

### 2. Tests de Integración (`@pytest.mark.integration`)

**Características:**
- Usan base de datos real (con rollback)
- Más lentos que tests unitarios
- Verifican interacción con infraestructura

**Ejemplo:**
```python
@pytest.mark.integration
@pytest.mark.asyncio
async def test_save_purchase_invoice(
    db_session,
    sample_purchase_invoice: PurchaseInvoice,
):
    # Arrange
    repository = PurchaseInvoiceRepositoryAdapter()

    # Act
    saved_invoice = await repository.save_purchase_invoice(sample_purchase_invoice)

    # Assert
    assert saved_invoice.id is not None
```

### 3. Tests End-to-End (`@pytest.mark.e2e`)

**Características:**
- Prueban flujos completos
- Incluyen múltiples componentes
- Los más lentos

---

## Configuración de Pytest

### pyproject.toml

```toml
[tool.pytest.ini_options]
asyncio_mode = "auto"           # Detecta automáticamente tests async
addopts = [
    "--verbose",                # Output detallado
    "--tb=short"                # Tracebacks cortos
]
pythonpath = ["."]
```

---

## Fixtures Globales

Definidas en `/backend/conftest.py`:

### Session Management

```python
@pytest.fixture
def session_context() -> str:
    """Crea un contexto de sesión único para cada test"""

@pytest.fixture
async def db_session(session_context) -> AsyncSession:
    """Proporciona una sesión de DB con rollback automático"""
```

**Uso:**
```python
async def test_something(db_session):
    # db_session ya tiene el contexto establecido
    # Todos los cambios se revierten al finalizar el test
    ...
```

### Faker

```python
@pytest.fixture(scope="session")
def fake() -> Faker:
    """Generador de datos aleatorios"""

@pytest.fixture
def random_email(fake: Faker) -> str:
    """Email aleatorio único"""

@pytest.fixture
def random_name(fake: Faker) -> str:
    """Nombre aleatorio"""
```

**Uso:**
```python
def test_create_user(fake, random_email):
    name = fake.name()
    email = random_email
    user = User(name=name, email=email)
```

### Mocks

```python
@pytest.fixture
def mock_repository() -> MagicMock:
    """Mock genérico de repositorio"""

@pytest.fixture
def mock_async_repository() -> AsyncMock:
    """Mock asíncrono de repositorio"""
```

---

## Fixtures por Módulo

Cada módulo puede definir sus propios fixtures en `test/conftest.py`:

### Ejemplo: modules/invoicing/test/conftest.py

```python
@pytest.fixture
def sample_purchase_invoice_data(fake: Faker) -> dict:
    """Datos de ejemplo para una factura"""
    return {
        "number": f"INV-{fake.random_int(min=1000, max=9999)}",
        "fk_provider": fake.random_int(min=1, max=100),
        "currency": "USD",
        # ...
    }

@pytest.fixture
def sample_purchase_invoice(sample_purchase_invoice_data: dict) -> PurchaseInvoice:
    """Instancia de PurchaseInvoice con datos de ejemplo"""
    return PurchaseInvoice(**sample_purchase_invoice_data)

@pytest.fixture
def mock_purchase_invoice_repository() -> AsyncMock:
    """Mock del repositorio de facturas"""
    return AsyncMock(spec=PurchaseInvoiceRepository)

@pytest.fixture
def purchase_invoice_service(mock_purchase_invoice_repository) -> PurchaseInvoiceService:
    """Servicio con repositorio mockeado"""
    return PurchaseInvoiceService(
        purchase_invoice_repository=mock_purchase_invoice_repository
    )
```

---

## Patrones de Testing

### Patrón AAA (Arrange-Act-Assert)

Todos los tests deben seguir este patrón:

```python
async def test_something():
    # Arrange - Preparar datos y mocks
    mock_repo.get_by_id.return_value = User(id=1, name="Test")
    service = UserService(mock_repo)

    # Act - Ejecutar la acción a testear
    result = await service.get_user(1)

    # Assert - Verificar resultados
    assert result.name == "Test"
    mock_repo.get_by_id.assert_called_once_with(1)
```

### Naming Convention

```python
# ✅ Bueno - Descriptivo y claro
async def test_save_purchase_invoice_assigns_id()
async def test_get_user_by_email_returns_none_when_not_found()
async def test_create_invoice_from_command_validates_data()

# ❌ Malo - Poco descriptivo
async def test_save()
async def test_user()
async def test_1()
```

### Docstrings en Tests

```python
async def test_something():
    """
    Test: Descripción breve del test.

    Given: Estado inicial
    When: Acción ejecutada
    Then: Resultado esperado
    """
    ...
```

---

## Ejecutar Tests

### Todos los tests

```bash
cd backend
pytest
```

### Solo tests unitarios

```bash
pytest -m unit
```

### Solo tests de integración

```bash
pytest -m integration
```

### Tests de un módulo específico

```bash
pytest modules/invoicing/test/
```

### Un archivo específico

```bash
pytest modules/invoicing/test/test_purchase_invoice_service.py
```

### Un test específico

```bash
pytest modules/invoicing/test/test_purchase_invoice_service.py::TestPurchaseInvoiceService::test_get_list_success
```

### Excluir tests lentos

```bash
pytest -m "not slow"
```

### Con coverage

```bash
pytest --cov=modules/invoicing --cov-report=html
```

### Verbose

```bash
pytest -v
pytest -vv  # Más verbose
```

### Ver output de print

```bash
pytest -s
```

### Detener en el primer fallo

```bash
pytest -x
```

### Ejecutar último test fallido

```bash
pytest --lf
```

---

## Marcadores Personalizados

### Disponibles

- `@pytest.mark.unit` - Test unitario (usa mocks)
- `@pytest.mark.integration` - Test de integración (usa DB)
- `@pytest.mark.e2e` - Test end-to-end
- `@pytest.mark.slow` - Test lento (puede excluirse)
- `@pytest.mark.asyncio` - Test asíncrono (automático con asyncio_mode="auto")

### Uso

```python
@pytest.mark.unit
@pytest.mark.asyncio
async def test_usecase_with_mock():
    ...

@pytest.mark.integration
@pytest.mark.slow
@pytest.mark.asyncio
async def test_full_flow_with_db():
    ...
```

---

## Estructura de Test Completa

### Ejemplo: Test de Repositorio

```python
"""
Tests para el repositorio de Purchase Invoice.
"""

import pytest
from modules.invoicing.domain.entity.purchase_invoice import PurchaseInvoice
from modules.invoicing.adapter.output.persistence.purchase_invoice_adapter import (
    PurchaseInvoiceRepositoryAdapter,
)


@pytest.mark.integration
@pytest.mark.asyncio
class TestPurchaseInvoiceRepository:
    """Suite de tests para PurchaseInvoiceRepository"""

    async def test_save_purchase_invoice(
        self,
        db_session,
        sample_purchase_invoice: PurchaseInvoice,
    ):
        """
        Test: Guardar una factura en la base de datos.

        Given: Una factura válida sin ID
        When: Se guarda en el repositorio
        Then: Se asigna un ID y se persiste
        """
        # Arrange
        repository = PurchaseInvoiceRepositoryAdapter()
        assert sample_purchase_invoice.id is None

        # Act
        saved = await repository.save_purchase_invoice(sample_purchase_invoice)

        # Assert
        assert saved.id is not None
        assert saved.number == sample_purchase_invoice.number
```

### Ejemplo: Test de Caso de Uso

```python
"""
Tests para casos de uso de Purchase Invoice.
"""

import pytest
from unittest.mock import AsyncMock
from modules.invoicing.domain.usecase.purchase_invoice import GetPurchaseInvoiceById


@pytest.mark.unit
@pytest.mark.asyncio
class TestGetPurchaseInvoiceById:
    """Tests para el caso de uso GetPurchaseInvoiceById"""

    async def test_get_invoice_by_id_success(
        self,
        mock_purchase_invoice_repository: AsyncMock,
        sample_purchase_invoice_with_id,
    ):
        """
        Test: Obtener factura por ID exitosamente.

        Given: Un repositorio que retorna una factura
        When: Se busca por ID
        Then: Se retorna la factura correcta
        """
        # Arrange
        invoice_id = 123
        mock_purchase_invoice_repository.get_purchase_invoice_by_id.return_value = sample_purchase_invoice_with_id
        usecase = GetPurchaseInvoiceById(mock_purchase_invoice_repository)

        # Act
        result = await usecase(id_purchase_invoice=invoice_id)

        # Assert
        assert result == sample_purchase_invoice_with_id
        mock_purchase_invoice_repository.get_purchase_invoice_by_id.assert_called_once_with(invoice_id)
```

### Ejemplo: Test de Servicio

```python
"""
Tests para el servicio de Purchase Invoice.
"""

import pytest
from unittest.mock import AsyncMock


@pytest.mark.unit
@pytest.mark.asyncio
class TestPurchaseInvoiceService:
    """Suite de tests para PurchaseInvoiceService"""

    async def test_get_list_success(
        self,
        purchase_invoice_service,
        mock_purchase_invoice_repository: AsyncMock,
        sample_purchase_invoice_with_id,
    ):
        """
        Test: Obtener lista de facturas.

        Given: Un servicio con facturas disponibles
        When: Se solicita la lista
        Then: Se retorna correctamente
        """
        # Arrange
        expected = [sample_purchase_invoice_with_id]
        mock_purchase_invoice_repository.get_purchase_invoice_list.return_value = expected

        # Act
        result = await purchase_invoice_service.get_list(limit=10, page=0)

        # Assert
        assert result == expected
```

---

## Best Practices

### ✅ DO

- Usar nombres descriptivos para tests
- Seguir patrón AAA (Arrange-Act-Assert)
- Un solo assert lógico por test
- Usar fixtures para datos de prueba
- Marcar tests con decoradores apropiados
- Aislar tests (no deben depender entre sí)
- Usar mocks para tests unitarios
- Cleanup automático con fixtures
- Documentar con docstrings Given-When-Then

### ❌ DON'T

- Hardcodear datos en tests
- Tests interdependientes
- Múltiples responsabilidades por test
- Ignorar tests fallidos
- Tests sin assertions
- Dejar datos basura en DB
- Tests sin documentación

---

## Troubleshooting

### Error: "session_context not set"

**Problema:** No se estableció el contexto de sesión.

**Solución:** Usa el fixture `session_context` o `db_session`:

```python
async def test_something(db_session):  # ✅
    ...
```

### Error: "Database has pending changes"

**Problema:** Cambios no revertidos en la DB.

**Solución:** Usa el fixture `db_session` que hace rollback automático:

```python
async def test_something(db_session):
    # Los cambios se revierten automáticamente
    ...
```

### Tests lentos

**Problema:** Los tests tardan mucho.

**Solución:**
1. Ejecutar solo tests unitarios: `pytest -m unit`
2. Excluir tests lentos: `pytest -m "not slow"`
3. Usar mocks en vez de DB real
4. Reducir cantidad de datos de prueba

### Import errors

**Problema:** No encuentra módulos.

**Solución:** Ejecutar desde el directorio `backend/`:

```bash
cd backend
pytest
```

---

## Coverage

### Generar reporte de cobertura

```bash
# HTML
pytest --cov=modules --cov-report=html

# Terminal
pytest --cov=modules --cov-report=term

# Ambos
pytest --cov=modules --cov-report=html --cov-report=term
```

### Ver reporte

```bash
# Abrir HTML
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
```

### Objetivo de cobertura

- **Repositorios:** 80%+
- **Casos de uso:** 90%+
- **Servicios:** 85%+
- **Tasks:** 70%+

---

## Integración Continua (CI)

### GitHub Actions (ejemplo)

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.12'
      - name: Install dependencies
        run: |
          pip install uv
          uv sync
      - name: Run tests
        run: |
          cd backend
          pytest -v --cov=modules --cov-report=xml
      - name: Upload coverage
        uses: codecov/codecov-action@v2
```

---

## Ejemplo Completo: Crear Tests para Nuevo Módulo

### Paso 1: Crear estructura

```bash
mkdir -p modules/mi_modulo/test
touch modules/mi_modulo/test/__init__.py
touch modules/mi_modulo/test/conftest.py
```

### Paso 2: Crear conftest.py

```python
# modules/mi_modulo/test/conftest.py
import pytest
from unittest.mock import AsyncMock
from modules.mi_modulo.domain.entity.mi_entidad import MiEntidad
from modules.mi_modulo.domain.repository.mi_repository import MiRepository

@pytest.fixture
def sample_mi_entidad_data(fake):
    return {
        "nombre": fake.name(),
        "email": fake.email(),
    }

@pytest.fixture
def sample_mi_entidad(sample_mi_entidad_data):
    return MiEntidad(**sample_mi_entidad_data)

@pytest.fixture
def mock_mi_repository():
    return AsyncMock(spec=MiRepository)
```

### Paso 3: Crear tests

```python
# modules/mi_modulo/test/test_mi_repository.py
import pytest

@pytest.mark.integration
@pytest.mark.asyncio
class TestMiRepository:
    async def test_save(self, db_session, sample_mi_entidad):
        ...
```

---

## Recursos

- [Pytest Documentation](https://docs.pytest.org/)
- [pytest-asyncio Documentation](https://pytest-asyncio.readthedocs.io/)
- [Faker Documentation](https://faker.readthedocs.io/)
- [unittest.mock Documentation](https://docs.python.org/3/library/unittest.mock.html)

---

**Última actualización:** 2025-10-23
