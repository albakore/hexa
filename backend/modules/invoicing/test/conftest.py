"""
Fixtures específicos para los tests del módulo invoicing.
"""

from datetime import date
from unittest.mock import AsyncMock

import pytest
from faker import Faker

from modules.invoicing.domain.entity.purchase_invoice import PurchaseInvoice
from modules.invoicing.domain.repository.purchase_invoice import (
	PurchaseInvoiceRepository,
)
from modules.invoicing.adapter.output.persistence.purchase_invoice_adapter import (
	PurchaseInvoiceRepositoryAdapter,
)
from modules.invoicing.application.service.purchase_invoice import (
	PurchaseInvoiceService,
)
from modules.invoicing.application.usecase.purchase_invoice import InvoiceUseCaseFactory

faker = Faker()


# ============================================================================
# ENTITY FACTORIES
# ============================================================================


@pytest.fixture
def sample_purchase_invoice_data(fake: Faker) -> dict:
	"""
	Crea datos de ejemplo para una factura de compra.

	Returns:
	    dict: Diccionario con datos de factura válidos
	"""
	return {
		"number": f"INV-{fake.random_int(min=1000, max=9999)}",
		"invoice_type": fake.random_element(["A", "B", "C"]),
		"fk_provider": fake.random_int(min=1, max=100),
		"branch": fake.city(),
		"region": fake.state(),
		"description": fake.sentence(),
		"concept": fake.word(),
		"country": fake.country_code(),
		"balance_year": str(fake.year()),
		"paid": False,
		"expense_mark": False,
		"applied_retentions": False,
		"issue_date": date.today(),
		"receipt_date": date.today(),
		"unit_price": float(fake.random_int(min=100, max=10000)),
		"currency": fake.random_element(["USD", "EUR", "ARS"]),
		"kilograms": float(fake.random_int(min=1, max=1000)),
		"items": fake.random_int(min=1, max=100),
	}


@pytest.fixture
def sample_purchase_invoice(sample_purchase_invoice_data: dict) -> PurchaseInvoice:
	"""
	Crea una instancia de PurchaseInvoice con datos de ejemplo.

	Args:
	    sample_purchase_invoice_data: Datos de la factura

	Returns:
	    PurchaseInvoice: Instancia de factura de compra
	"""
	return PurchaseInvoice(**sample_purchase_invoice_data)


@pytest.fixture
def sample_purchase_invoice_with_id(
	sample_purchase_invoice_data: dict, random_int: int
) -> PurchaseInvoice:
	"""
	Crea una instancia de PurchaseInvoice con ID (simulando una factura guardada).

	Args:
	    sample_purchase_invoice_data: Datos de la factura
	    random_int: ID aleatorio

	Returns:
	    PurchaseInvoice: Instancia de factura con ID
	"""
	data = {**sample_purchase_invoice_data, "id": random_int}
	return PurchaseInvoice(**data)


# ============================================================================
# REPOSITORY FIXTURES
# ============================================================================


@pytest.fixture
def mock_purchase_invoice_repository() -> AsyncMock:
	"""
	Mock del repositorio de facturas de compra.

	Returns:
	    AsyncMock: Mock con los métodos del repositorio
	"""
	mock = AsyncMock(spec=PurchaseInvoiceRepository)
	return mock


@pytest.fixture
def real_purchase_invoice_repository(db_session) -> PurchaseInvoiceRepositoryAdapter:
	"""
	Repositorio real de facturas de compra conectado a la base de datos de test.

	Args:
	    db_session: Sesión de base de datos de test

	Returns:
	    PurchaseInvoiceRepositoryAdapter: Instancia real del repositorio
	"""
	from modules.invoicing.adapter.output.persistence.sqlalchemy.purchase_invoice import (
		PurchaseInvoiceSQLAlchemyRepository,
	)

	# Inyectar el repositorio SQLAlchemy real
	sqlalchemy_repo = PurchaseInvoiceSQLAlchemyRepository()
	return PurchaseInvoiceRepositoryAdapter(repository=sqlalchemy_repo)


# ============================================================================
# USE CASE FIXTURES
# ============================================================================


@pytest.fixture
def invoice_usecase_factory(
	mock_purchase_invoice_repository: AsyncMock,
) -> InvoiceUseCaseFactory:
	"""
	Factory de casos de uso con repositorio mockeado.

	Args:
	    mock_purchase_invoice_repository: Repositorio mockeado

	Returns:
	    InvoiceUseCaseFactory: Factory de casos de uso
	"""
	return InvoiceUseCaseFactory(mock_purchase_invoice_repository)


# ============================================================================
# SERVICE FIXTURES
# ============================================================================


@pytest.fixture
def purchase_invoice_service(
	mock_purchase_invoice_repository: AsyncMock,
) -> PurchaseInvoiceService:
	"""
	Servicio de facturas de compra con repositorio mockeado.

	Args:
	    mock_purchase_invoice_repository: Repositorio mockeado

	Returns:
	    PurchaseInvoiceService: Instancia del servicio
	"""
	return PurchaseInvoiceService(
		purchase_invoice_repository=mock_purchase_invoice_repository
	)


@pytest.fixture
def real_purchase_invoice_service(
	real_purchase_invoice_repository: PurchaseInvoiceRepositoryAdapter,
) -> PurchaseInvoiceService:
	"""
	Servicio de facturas de compra con repositorio real (para tests de integración).

	Args:
	    real_purchase_invoice_repository: Repositorio real

	Returns:
	    PurchaseInvoiceService: Instancia del servicio
	"""
	return PurchaseInvoiceService(
		purchase_invoice_repository=real_purchase_invoice_repository
	)
