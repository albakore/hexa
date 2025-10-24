"""
Tests para el servicio de Purchase Invoice.

Estos son tests unitarios que verifican la lógica del servicio usando mocks.
"""

import pytest
from datetime import date
from unittest.mock import AsyncMock
import uuid

from modules.invoicing.application.service.purchase_invoice import PurchaseInvoiceService
from modules.invoicing.application.command import CreatePurchaseInvoiceCommand
from modules.invoicing.domain.entity.purchase_invoice import PurchaseInvoice


@pytest.mark.unit
@pytest.mark.asyncio
class TestPurchaseInvoiceService:
    """Suite de tests para PurchaseInvoiceService"""

    async def test_get_list_success(
        self,
        purchase_invoice_service: PurchaseInvoiceService,
        mock_purchase_invoice_repository: AsyncMock,
        sample_purchase_invoice_with_id: PurchaseInvoice,
    ):
        """
        Test: Obtener lista de facturas exitosamente.

        Given: Un servicio con facturas disponibles
        When: Se solicita la lista
        Then: Se retorna la lista correctamente
        """
        # Arrange
        expected_invoices = [sample_purchase_invoice_with_id]
        mock_purchase_invoice_repository.get_purchase_invoice_list.return_value = expected_invoices

        # Act
        result = await purchase_invoice_service.get_list(limit=10, page=0)

        # Assert
        assert result == expected_invoices
        mock_purchase_invoice_repository.get_purchase_invoice_list.assert_called_once_with(10, 0)

    async def test_get_list_of_provider_success(
        self,
        purchase_invoice_service: PurchaseInvoiceService,
        mock_purchase_invoice_repository: AsyncMock,
        sample_purchase_invoice_with_id: PurchaseInvoice,
    ):
        """
        Test: Obtener facturas de un proveedor específico.

        Given: Un servicio con facturas de un proveedor
        When: Se solicita la lista de ese proveedor
        Then: Se retornan solo las facturas del proveedor
        """
        # Arrange
        provider_id = 42
        expected_invoices = [sample_purchase_invoice_with_id]
        mock_purchase_invoice_repository.get_purchase_invoice_list_by_provider.return_value = expected_invoices

        # Act
        result = await purchase_invoice_service.get_list_of_provider(
            id_provider=provider_id,
            limit=10,
            page=0
        )

        # Assert
        assert result == expected_invoices
        mock_purchase_invoice_repository.get_purchase_invoice_list_by_provider.assert_called_once_with(
            provider_id, 10, 0
        )

    async def test_get_one_by_id_success(
        self,
        purchase_invoice_service: PurchaseInvoiceService,
        mock_purchase_invoice_repository: AsyncMock,
        sample_purchase_invoice_with_id: PurchaseInvoice,
    ):
        """
        Test: Obtener una factura por ID.

        Given: Un ID de factura existente
        When: Se solicita la factura
        Then: Se retorna la factura correcta
        """
        # Arrange
        invoice_id = 123
        mock_purchase_invoice_repository.get_purchase_invoice_by_id.return_value = sample_purchase_invoice_with_id

        # Act
        result = await purchase_invoice_service.get_one_by_id(id_purchase_invoice=invoice_id)

        # Assert
        assert result == sample_purchase_invoice_with_id
        mock_purchase_invoice_repository.get_purchase_invoice_by_id.assert_called_once_with(invoice_id)

    async def test_get_one_by_id_not_found(
        self,
        purchase_invoice_service: PurchaseInvoiceService,
        mock_purchase_invoice_repository: AsyncMock,
    ):
        """
        Test: Buscar factura que no existe.

        Given: Un ID de factura inexistente
        When: Se solicita la factura
        Then: Se retorna None
        """
        # Arrange
        invoice_id = 999999
        mock_purchase_invoice_repository.get_purchase_invoice_by_id.return_value = None

        # Act
        result = await purchase_invoice_service.get_one_by_id(id_purchase_invoice=invoice_id)

        # Assert
        assert result is None

    async def test_create_invoice_from_command(
        self,
        purchase_invoice_service: PurchaseInvoiceService,
        fake,
    ):
        """
        Test: Crear instancia de factura desde comando.

        Given: Un comando válido de creación
        When: Se ejecuta el método create
        Then: Se retorna una instancia de PurchaseInvoice
        """
        # Arrange
        command = CreatePurchaseInvoiceCommand(
            fk_provider=1,
            fk_service=1,
            number=f"INV-{fake.random_int(min=1000, max=9999)}",
            concept="Test invoice",
            issue_date=date.today(),
            receipt_date=date.today(),
            service_month=date.today(),
            currency="USD",
            unit_price=100.50,
            fk_receipt_file=uuid.uuid4(),
        )

        # Act
        result = await purchase_invoice_service.create(command)

        # Assert
        assert isinstance(result, PurchaseInvoice)
        assert result.number == command.number
        assert result.fk_provider == command.fk_provider
        assert result.concept == command.concept
        assert result.currency == command.currency
        assert result.unit_price == command.unit_price
        assert result.id is None  # No debe tener ID aún

    async def test_save_invoice_success(
        self,
        purchase_invoice_service: PurchaseInvoiceService,
        mock_purchase_invoice_repository: AsyncMock,
        sample_purchase_invoice: PurchaseInvoice,
        sample_purchase_invoice_with_id: PurchaseInvoice,
    ):
        """
        Test: Guardar factura exitosamente.

        Given: Una factura válida
        When: Se guarda la factura
        Then: Se retorna la factura con ID asignado
        """
        # Arrange
        mock_purchase_invoice_repository.save_purchase_invoice.return_value = sample_purchase_invoice_with_id

        # Act
        result = await purchase_invoice_service.save(sample_purchase_invoice)

        # Assert
        assert result.id is not None
        assert result.id == sample_purchase_invoice_with_id.id
        mock_purchase_invoice_repository.save_purchase_invoice.assert_called_once_with(sample_purchase_invoice)

    async def test_create_and_save_flow(
        self,
        purchase_invoice_service: PurchaseInvoiceService,
        mock_purchase_invoice_repository: AsyncMock,
        fake,
    ):
        """
        Test: Flujo completo de crear y guardar factura.

        Given: Un comando de creación válido
        When: Se crea y luego se guarda la factura
        Then: El flujo completo funciona correctamente
        """
        # Arrange
        command = CreatePurchaseInvoiceCommand(
            fk_provider=1,
            fk_service=1,
            number=f"INV-{fake.random_int(min=1000, max=9999)}",
            concept="Test invoice",
            issue_date=date.today(),
            receipt_date=date.today(),
            service_month=date.today(),
            currency="USD",
            unit_price=100.50,
            fk_receipt_file=uuid.uuid4(),
        )

        # Mock para que save retorne la factura con ID
        def save_side_effect(invoice):
            saved = invoice.model_copy()
            saved.id = 123
            return saved

        mock_purchase_invoice_repository.save_purchase_invoice.side_effect = save_side_effect

        # Act
        # Paso 1: Crear factura desde comando
        invoice = await purchase_invoice_service.create(command)
        assert invoice.id is None

        # Paso 2: Guardar factura
        saved_invoice = await purchase_invoice_service.save(invoice)

        # Assert
        assert saved_invoice.id == 123
        assert saved_invoice.number == command.number
        assert saved_invoice.fk_provider == command.fk_provider


@pytest.mark.integration
@pytest.mark.asyncio
class TestPurchaseInvoiceServiceIntegration:
    """Tests de integración para el servicio con repositorio real"""

    async def test_full_flow_with_real_repository(
        self,
        real_purchase_invoice_service: PurchaseInvoiceService,
        fake,
        db_session,
    ):
        """
        Test de integración: Flujo completo con repositorio real.

        Given: Un servicio con repositorio real
        When: Se crea, guarda y consulta una factura
        Then: Todo el flujo funciona correctamente
        """
        # Arrange
        command = CreatePurchaseInvoiceCommand(
            fk_provider=1,
            fk_service=1,
            number=f"INV-INTEGRATION-{fake.random_int(min=1000, max=9999)}",
            concept="Integration test invoice",
            issue_date=date.today(),
            receipt_date=date.today(),
            service_month=date.today(),
            currency="USD",
            unit_price=150.75,
            fk_receipt_file=uuid.uuid4(),
            items=5,
            kilograms=10.5,
        )

        # Act
        # Paso 1: Crear factura
        invoice = await real_purchase_invoice_service.create(command)
        assert invoice.id is None

        # Paso 2: Guardar factura
        saved_invoice = await real_purchase_invoice_service.save(invoice)
        assert saved_invoice.id is not None
        invoice_id = saved_invoice.id

        # Paso 3: Consultar factura
        retrieved_invoice = await real_purchase_invoice_service.get_one_by_id(invoice_id)

        # Assert
        assert retrieved_invoice is not None
        assert retrieved_invoice.id == invoice_id
        assert retrieved_invoice.number == command.number
        assert retrieved_invoice.concept == command.concept
        assert retrieved_invoice.currency == command.currency
        assert retrieved_invoice.unit_price == command.unit_price
        assert retrieved_invoice.items == command.items
        assert retrieved_invoice.kilograms == command.kilograms

    async def test_get_list_with_real_repository(
        self,
        real_purchase_invoice_service: PurchaseInvoiceService,
        fake,
        db_session,
    ):
        """
        Test de integración: Obtener lista con repositorio real.

        Given: Múltiples facturas guardadas
        When: Se solicita la lista
        Then: Se retornan correctamente
        """
        # Arrange - Crear y guardar 3 facturas
        for i in range(3):
            command = CreatePurchaseInvoiceCommand(
                fk_provider=1,
                fk_service=1,
                number=f"INV-LIST-{i}-{fake.random_int(min=1000, max=9999)}",
                concept=f"Test {i}",
                issue_date=date.today(),
                receipt_date=date.today(),
                service_month=date.today(),
                currency="USD",
                unit_price=100.0 * (i + 1),
                fk_receipt_file=uuid.uuid4(),
            )
            invoice = await real_purchase_invoice_service.create(command)
            await real_purchase_invoice_service.save(invoice)

        # Act
        result = await real_purchase_invoice_service.get_list(limit=10, page=0)

        # Assert
        assert len(result) >= 3
        assert all(isinstance(inv, PurchaseInvoice) for inv in result)
