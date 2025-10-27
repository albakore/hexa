"""
Tests para los casos de uso de Purchase Invoice.

Estos son tests unitarios que verifican la lógica de negocio usando mocks.
"""

import pytest
from unittest.mock import AsyncMock

from modules.invoicing.domain.entity.purchase_invoice import PurchaseInvoice
from modules.invoicing.domain.usecase.purchase_invoice import (
    GetPurchaseInvoiceList,
    GetPurchaseInvoiceListByProvider,
    GetPurchaseInvoiceById,
    SavePurchaseInvoice,
    InvoiceUseCaseFactory,
)


@pytest.mark.unit
@pytest.mark.asyncio
class TestGetPurchaseInvoiceList:
    """Tests para el caso de uso GetPurchaseInvoiceList"""

    async def test_get_purchase_invoice_list_success(
        self,
        mock_purchase_invoice_repository: AsyncMock,
        sample_purchase_invoice_with_id: PurchaseInvoice,
    ):
        """
        Test: Obtener lista de facturas exitosamente.

        Given: Un repositorio que retorna una lista de facturas
        When: Se ejecuta el caso de uso
        Then: Se retorna la lista correctamente
        """
        # Arrange
        expected_invoices = [sample_purchase_invoice_with_id]
        mock_purchase_invoice_repository.get_purchase_invoice_list.return_value = expected_invoices

        usecase = GetPurchaseInvoiceList(mock_purchase_invoice_repository)

        # Act
        result = await usecase(limit=10, page=0)

        # Assert
        assert result == expected_invoices
        mock_purchase_invoice_repository.get_purchase_invoice_list.assert_called_once_with(10, 0)

    async def test_get_purchase_invoice_list_empty(
        self,
        mock_purchase_invoice_repository: AsyncMock,
    ):
        """
        Test: Obtener lista vacía cuando no hay facturas.

        Given: Un repositorio que retorna lista vacía
        When: Se ejecuta el caso de uso
        Then: Se retorna lista vacía
        """
        # Arrange
        mock_purchase_invoice_repository.get_purchase_invoice_list.return_value = []
        usecase = GetPurchaseInvoiceList(mock_purchase_invoice_repository)

        # Act
        result = await usecase(limit=10, page=0)

        # Assert
        assert result == []
        assert len(result) == 0

    async def test_get_purchase_invoice_list_with_pagination(
        self,
        mock_purchase_invoice_repository: AsyncMock,
        sample_purchase_invoice_with_id: PurchaseInvoice,
    ):
        """
        Test: Verificar que se pasan correctamente los parámetros de paginación.

        Given: Parámetros de límite y página
        When: Se ejecuta el caso de uso
        Then: Se pasan correctamente al repositorio
        """
        # Arrange
        mock_purchase_invoice_repository.get_purchase_invoice_list.return_value = [sample_purchase_invoice_with_id]
        usecase = GetPurchaseInvoiceList(mock_purchase_invoice_repository)

        # Act
        await usecase(limit=50, page=2)

        # Assert
        mock_purchase_invoice_repository.get_purchase_invoice_list.assert_called_once_with(50, 2)


@pytest.mark.unit
@pytest.mark.asyncio
class TestGetPurchaseInvoiceListByProvider:
    """Tests para el caso de uso GetPurchaseInvoiceListByProvider"""

    async def test_get_invoices_by_provider_success(
        self,
        mock_purchase_invoice_repository: AsyncMock,
        sample_purchase_invoice_with_id: PurchaseInvoice,
    ):
        """
        Test: Obtener facturas de un proveedor específico.

        Given: Un ID de proveedor y facturas asociadas
        When: Se ejecuta el caso de uso
        Then: Se retornan las facturas del proveedor
        """
        # Arrange
        provider_id = 42
        expected_invoices = [sample_purchase_invoice_with_id]
        mock_purchase_invoice_repository.get_purchase_invoice_list_by_provider.return_value = expected_invoices

        usecase = GetPurchaseInvoiceListByProvider(mock_purchase_invoice_repository)

        # Act
        result = await usecase(id_provider=provider_id, limit=10, page=0)

        # Assert
        assert result == expected_invoices
        mock_purchase_invoice_repository.get_purchase_invoice_list_by_provider.assert_called_once_with(
            provider_id, 10, 0
        )

    async def test_get_invoices_by_provider_not_found(
        self,
        mock_purchase_invoice_repository: AsyncMock,
    ):
        """
        Test: Buscar facturas de un proveedor sin facturas.

        Given: Un proveedor sin facturas asociadas
        When: Se ejecuta el caso de uso
        Then: Se retorna lista vacía
        """
        # Arrange
        provider_id = 999
        mock_purchase_invoice_repository.get_purchase_invoice_list_by_provider.return_value = []

        usecase = GetPurchaseInvoiceListByProvider(mock_purchase_invoice_repository)

        # Act
        result = await usecase(id_provider=provider_id, limit=10, page=0)

        # Assert
        assert result == []


@pytest.mark.unit
@pytest.mark.asyncio
class TestGetPurchaseInvoiceById:
    """Tests para el caso de uso GetPurchaseInvoiceById"""

    async def test_get_invoice_by_id_success(
        self,
        mock_purchase_invoice_repository: AsyncMock,
        sample_purchase_invoice_with_id: PurchaseInvoice,
    ):
        """
        Test: Obtener factura por ID exitosamente.

        Given: Un ID de factura existente
        When: Se ejecuta el caso de uso
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

    async def test_get_invoice_by_id_not_found(
        self,
        mock_purchase_invoice_repository: AsyncMock,
    ):
        """
        Test: Buscar factura que no existe.

        Given: Un ID de factura inexistente
        When: Se ejecuta el caso de uso
        Then: Se retorna None
        """
        # Arrange
        invoice_id = 999999
        mock_purchase_invoice_repository.get_purchase_invoice_by_id.return_value = None

        usecase = GetPurchaseInvoiceById(mock_purchase_invoice_repository)

        # Act
        result = await usecase(id_purchase_invoice=invoice_id)

        # Assert
        assert result is None


@pytest.mark.unit
@pytest.mark.asyncio
class TestSavePurchaseInvoice:
    """Tests para el caso de uso SavePurchaseInvoice"""

    async def test_save_new_invoice_success(
        self,
        mock_purchase_invoice_repository: AsyncMock,
        sample_purchase_invoice: PurchaseInvoice,
        sample_purchase_invoice_with_id: PurchaseInvoice,
    ):
        """
        Test: Guardar nueva factura exitosamente.

        Given: Una factura nueva sin ID
        When: Se ejecuta el caso de uso
        Then: Se guarda y se retorna con ID asignado
        """
        # Arrange
        mock_purchase_invoice_repository.save_purchase_invoice.return_value = sample_purchase_invoice_with_id

        usecase = SavePurchaseInvoice(mock_purchase_invoice_repository)

        # Act
        result = await usecase(purchase_invoice=sample_purchase_invoice)

        # Assert
        assert result.id is not None
        assert result.id == sample_purchase_invoice_with_id.id
        mock_purchase_invoice_repository.save_purchase_invoice.assert_called_once_with(sample_purchase_invoice)

    async def test_update_existing_invoice(
        self,
        mock_purchase_invoice_repository: AsyncMock,
        sample_purchase_invoice_with_id: PurchaseInvoice,
    ):
        """
        Test: Actualizar factura existente.

        Given: Una factura con ID (ya guardada)
        When: Se ejecuta el caso de uso
        Then: Se actualiza correctamente
        """
        # Arrange
        updated_invoice = sample_purchase_invoice_with_id.model_copy()
        updated_invoice.paid = True

        mock_purchase_invoice_repository.save_purchase_invoice.return_value = updated_invoice

        usecase = SavePurchaseInvoice(mock_purchase_invoice_repository)

        # Act
        result = await usecase(purchase_invoice=updated_invoice)

        # Assert
        assert result.paid is True
        assert result.id == sample_purchase_invoice_with_id.id


@pytest.mark.unit
@pytest.mark.asyncio
class TestInvoiceUseCaseFactory:
    """Tests para InvoiceUseCaseFactory"""

    def test_factory_creates_all_usecases(
        self,
        mock_purchase_invoice_repository: AsyncMock,
    ):
        """
        Test: Verificar que la factory crea todos los casos de uso.

        Given: Un repositorio
        When: Se instancia la factory
        Then: Todos los casos de uso están disponibles
        """
        # Act
        factory = InvoiceUseCaseFactory(mock_purchase_invoice_repository)

        # Assert
        assert isinstance(factory.get_purchase_invoice_list, GetPurchaseInvoiceList)
        assert isinstance(factory.get_purchase_invoice_list_by_provider, GetPurchaseInvoiceListByProvider)
        assert isinstance(factory.get_purchase_invoice_by_id, GetPurchaseInvoiceById)
        assert isinstance(factory.save_purchase_invoice, SavePurchaseInvoice)

    async def test_factory_usecases_are_functional(
        self,
        mock_purchase_invoice_repository: AsyncMock,
        sample_purchase_invoice_with_id: PurchaseInvoice,
    ):
        """
        Test: Verificar que los casos de uso de la factory funcionan.

        Given: Una factory con casos de uso
        When: Se ejecuta un caso de uso
        Then: Funciona correctamente
        """
        # Arrange
        mock_purchase_invoice_repository.get_purchase_invoice_by_id.return_value = sample_purchase_invoice_with_id
        factory = InvoiceUseCaseFactory(mock_purchase_invoice_repository)

        # Act
        result = await factory.get_purchase_invoice_by_id(123)

        # Assert
        assert result == sample_purchase_invoice_with_id