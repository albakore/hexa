"""
Tests para las tareas de Celery del módulo invoicing.

Las tasks refactorizadas son funciones Python normales, por lo que son fáciles de testear.
"""

import pytest
from modules.invoicing.adapter.input.tasks.invoice import emit_invoice


@pytest.mark.unit
class TestInvoicingTasks:
    """Tests para las tasks de Celery de invoicing"""

    def test_emit_invoice_returns_message(self):
        """
        Test: La task emit_invoice retorna un mensaje.

        Given: La task emit_invoice
        When: Se ejecuta directamente (sin Celery)
        Then: Retorna el mensaje esperado
        """
        # Act
        result = emit_invoice()

        # Assert
        assert result is not None
        assert isinstance(result, str)
        assert len(result) > 0

    def test_emit_invoice_is_callable(self):
        """
        Test: La task es un callable que puede ser registrado en Celery.

        Given: La función emit_invoice
        When: Se verifica si es callable
        Then: Es callable
        """
        # Assert
        assert callable(emit_invoice)

    @pytest.mark.slow
    def test_emit_invoice_execution_time(self):
        """
        Test: La task tarda aproximadamente 10 segundos (tiene sleep).

        Given: La task con sleep(10)
        When: Se ejecuta
        Then: Tarda aproximadamente 10 segundos

        Note: Este test está marcado como slow
        """
        import time

        # Act
        start = time.time()
        result = emit_invoice()
        elapsed = time.time() - start

        # Assert
        assert result is not None
        assert elapsed >= 9.5  # Al menos 9.5 segundos (margen de error)
        assert elapsed <= 11.0  # Máximo 11 segundos

    def test_emit_invoice_can_be_registered_as_celery_task(self):
        """
        Test: Verificar que la función puede ser decorada como task de Celery.

        Given: La función emit_invoice
        When: Se simula el registro en Celery
        Then: No genera errores
        """
        from celery import Celery

        # Arrange
        app = Celery()

        # Act - Registrar como task
        task = app.task(name="test.emit_invoice")(emit_invoice)

        # Assert
        assert task is not None
        assert task.name == "test.emit_invoice"
