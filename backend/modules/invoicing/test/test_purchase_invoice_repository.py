"""
Tests para el repositorio de Purchase Invoice.

Estos son tests de integración que verifican la interacción con la base de datos.
"""

import pytest
from sqlalchemy import select

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
		real_purchase_invoice_repository: PurchaseInvoiceRepositoryAdapter,
		sample_purchase_invoice: PurchaseInvoice,
	):
		"""
		Test: Guardar una factura de compra en la base de datos.

		Given: Una factura de compra válida
		When: Se guarda en el repositorio
		Then: La factura se guarda correctamente y se le asigna un ID
		"""
		# Arrange
		assert sample_purchase_invoice.id is None

		# Act
		saved_invoice = await real_purchase_invoice_repository.save_purchase_invoice(
			sample_purchase_invoice
		)

		# Assert
		assert saved_invoice.id is not None
		assert saved_invoice.number == sample_purchase_invoice.number
		assert saved_invoice.fk_provider == sample_purchase_invoice.fk_provider
		assert saved_invoice.currency == sample_purchase_invoice.currency

	async def test_get_purchase_invoice_by_id(
		self,
		db_session,
		real_purchase_invoice_repository: PurchaseInvoiceRepositoryAdapter,
		sample_purchase_invoice: PurchaseInvoice,
	):
		"""
		Test: Obtener una factura por ID.

		Given: Una factura guardada en la base de datos
		When: Se busca por su ID
		Then: Se retorna la factura correcta
		"""
		# Arrange
		repository = real_purchase_invoice_repository
		saved_invoice = await repository.save_purchase_invoice(sample_purchase_invoice)
		invoice_id = saved_invoice.id

		# Act
		retrieved_invoice = await repository.get_purchase_invoice_by_id(invoice_id)

		# Assert
		assert retrieved_invoice is not None
		assert retrieved_invoice.id == invoice_id
		assert retrieved_invoice.number == sample_purchase_invoice.number

	async def test_get_purchase_invoice_by_id_not_found(
		self,
		db_session,
		real_purchase_invoice_repository: PurchaseInvoiceRepositoryAdapter,
	):
		"""
		Test: Buscar una factura que no existe.

		Given: Un ID que no existe en la base de datos
		When: Se busca la factura
		Then: Se retorna None
		"""
		# Arrange
		repository = real_purchase_invoice_repository
		non_existent_id = 999999

		# Act
		result = await repository.get_purchase_invoice_by_id(non_existent_id)

		# Assert
		assert result is None

	async def test_get_purchase_invoice_list(
		self,
		db_session,
		real_purchase_invoice_repository: PurchaseInvoiceRepositoryAdapter,
		sample_purchase_invoice: PurchaseInvoice,
		fake,
	):
		"""
		Test: Obtener lista paginada de facturas.

		Given: Varias facturas en la base de datos
		When: Se solicita una lista con límite y página
		Then: Se retorna la lista correcta
		"""
		# Arrange
		repository = real_purchase_invoice_repository

		# Crear 5 facturas
		invoices = []
		for i in range(5):
			invoice_data = sample_purchase_invoice.model_dump(exclude={"id"})
			invoice_data["number"] = f"INV-{fake.random_int(min=1000, max=9999)}"
			invoice = PurchaseInvoice(**invoice_data)
			saved = await repository.save_purchase_invoice(invoice)
			invoices.append(saved)

		# Act
		result = await repository.get_purchase_invoice_list(limit=3, page=0)

		# Assert
		assert len(result) <= 3
		assert all(isinstance(inv, PurchaseInvoice) for inv in result)

	async def test_get_purchase_invoice_list_pagination(
		self,
		db_session,
		real_purchase_invoice_repository: PurchaseInvoiceRepositoryAdapter,
		sample_purchase_invoice: PurchaseInvoice,
		fake,
	):
		"""
		Test: Verificar que la paginación funciona correctamente.

		Given: 10 facturas en la base de datos
		When: Se solicita la página 0 y la página 1 con límite 5
		Then: Las páginas no deben tener elementos repetidos
		"""
		# Arrange
		repository = real_purchase_invoice_repository

		# Crear 10 facturas
		for i in range(10):
			invoice_data = sample_purchase_invoice.model_dump(exclude={"id"})
			invoice_data["number"] = f"INV-PAGINATION-{i}"
			invoice = PurchaseInvoice(**invoice_data)
			await repository.save_purchase_invoice(invoice)

		# Act
		page_0 = await repository.get_purchase_invoice_list(limit=5, page=0)
		page_1 = await repository.get_purchase_invoice_list(limit=5, page=1)

		# Assert
		assert len(page_0) == 5
		assert len(page_1) == 5

		# Los IDs no deben repetirse
		ids_page_0 = {inv.id for inv in page_0}
		ids_page_1 = {inv.id for inv in page_1}
		assert ids_page_0.isdisjoint(ids_page_1)

	async def test_get_purchase_invoice_list_by_provider(
		self,
		db_session,
		real_purchase_invoice_repository: PurchaseInvoiceRepositoryAdapter,
		sample_purchase_invoice: PurchaseInvoice,
		fake,
	):
		"""
		Test: Obtener facturas filtradas por proveedor.

		Given: Facturas de diferentes proveedores
		When: Se solicita la lista de un proveedor específico
		Then: Solo se retornan facturas de ese proveedor
		"""
		# Arrange
		repository = real_purchase_invoice_repository
		target_provider_id = 42

		# Crear 3 facturas del proveedor target
		for i in range(3):
			invoice_data = sample_purchase_invoice.model_dump(exclude={"id"})
			invoice_data["number"] = f"INV-PROV42-{i}"
			invoice_data["fk_provider"] = target_provider_id
			invoice = PurchaseInvoice(**invoice_data)
			await repository.save_purchase_invoice(invoice)

		# Crear 2 facturas de otro proveedor
		for i in range(2):
			invoice_data = sample_purchase_invoice.model_dump(exclude={"id"})
			invoice_data["number"] = f"INV-PROV99-{i}"
			invoice_data["fk_provider"] = 99
			invoice = PurchaseInvoice(**invoice_data)
			await repository.save_purchase_invoice(invoice)

		# Act
		result = await repository.get_purchase_invoice_list_by_provider(
			id_provider=target_provider_id, limit=10, page=0
		)

		# Assert
		assert len(result) == 3
		assert all(inv.fk_provider == target_provider_id for inv in result)

	async def test_update_purchase_invoice(
		self,
		db_session,
		real_purchase_invoice_repository: PurchaseInvoiceRepositoryAdapter,
		sample_purchase_invoice: PurchaseInvoice,
	):
		"""
		Test: Actualizar una factura existente.

		Given: Una factura guardada
		When: Se modifican sus campos y se guarda nuevamente
		Then: Los cambios se persisten correctamente
		"""
		# Arrange
		repository = real_purchase_invoice_repository
		saved_invoice = await repository.save_purchase_invoice(sample_purchase_invoice)
		invoice_id = saved_invoice.id

		# Modificar campos
		saved_invoice.paid = True
		saved_invoice.description = "Updated description"
		saved_invoice.unit_price = 999.99

		# Act
		updated_invoice = await repository.save_purchase_invoice(saved_invoice)

		# Assert
		assert updated_invoice.id == invoice_id
		assert updated_invoice.paid is True
		assert updated_invoice.description == "Updated description"
		assert updated_invoice.unit_price == 999.99

		# Verificar que se actualizó en DB
		retrieved = await repository.get_purchase_invoice_by_id(invoice_id)
		assert retrieved.paid is True
		assert retrieved.description == "Updated description"
