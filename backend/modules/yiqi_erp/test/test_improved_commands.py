"""
Tests for improved Yiqi commands using Pydantic v2.

Demonstrates how the new validation makes testing easier and more thorough.
"""

import pytest
from datetime import date, timedelta
from decimal import Decimal
from io import BytesIO

from modules.yiqi_erp.domain.command.improved_commands import (
    CreateYiqiInvoiceCommand,
    UploadFileCommand,
    YiqiInvoiceBase,
    PositiveInt,
    PositiveDecimal,
    AWBString,
)


# === Fixtures ===

@pytest.fixture
def valid_invoice_data():
    """Provide valid invoice data for testing."""
    return {
        "Provider": 123,
        "Numero": "001-001-0000001",
        "Concepto": "Servicios de transporte aéreo internacional",
        "Fecha_emision": date(2024, 1, 15),
        "Fecha_recepcion": date(2024, 1, 16),
        "Mes_servicio": date(2024, 1, 1),
        "Precio_unitario": Decimal("1500.50"),
        "Moneda_original": 2,
        "Servicio": 456,
        "creado_en_portal": True,
    }


@pytest.fixture
def valid_invoice_with_optionals(valid_invoice_data):
    """Provide valid invoice data with all optional fields."""
    return {
        **valid_invoice_data,
        "AWB": "123-45678901",
        "Kg": 50.5,
        "Items": 10,
    }


# === Test Basic Field Validation ===

class TestBasicFieldValidation:
    """Test individual field validators."""

    def test_create_valid_invoice(self, valid_invoice_data):
        """Test creating invoice with valid data."""
        invoice = CreateYiqiInvoiceCommand(**valid_invoice_data)

        assert invoice.Provider == 123
        assert invoice.Numero == "001-001-0000001"
        assert invoice.Precio_unitario == Decimal("1500.50")

    def test_provider_must_be_positive(self, valid_invoice_data):
        """Test Provider must be positive integer."""
        valid_invoice_data["Provider"] = 0

        with pytest.raises(ValueError, match="greater than 0"):
            CreateYiqiInvoiceCommand(**valid_invoice_data)

    def test_numero_cannot_be_empty(self, valid_invoice_data):
        """Test invoice number cannot be empty."""
        valid_invoice_data["Numero"] = ""

        with pytest.raises(ValueError, match="cannot be empty"):
            CreateYiqiInvoiceCommand(**valid_invoice_data)

    def test_numero_too_short(self, valid_invoice_data):
        """Test invoice number must have minimum length."""
        valid_invoice_data["Numero"] = "AB"

        with pytest.raises(ValueError, match="too short"):
            CreateYiqiInvoiceCommand(**valid_invoice_data)

    def test_concepto_cannot_be_empty(self, valid_invoice_data):
        """Test concept cannot be empty."""
        valid_invoice_data["Concepto"] = "   "

        with pytest.raises(ValueError, match="cannot be empty"):
            CreateYiqiInvoiceCommand(**valid_invoice_data)

    def test_concepto_too_short(self, valid_invoice_data):
        """Test concept must have meaningful length."""
        valid_invoice_data["Concepto"] = "ABC"

        with pytest.raises(ValueError, match="too short"):
            CreateYiqiInvoiceCommand(**valid_invoice_data)

    def test_precio_must_be_positive(self, valid_invoice_data):
        """Test price must be positive."""
        valid_invoice_data["Precio_unitario"] = Decimal("-100")

        with pytest.raises(ValueError, match="greater than 0"):
            CreateYiqiInvoiceCommand(**valid_invoice_data)


# === Test Date Validation ===

class TestDateValidation:
    """Test date field validators."""

    def test_date_string_format_yyyy_mm_dd(self, valid_invoice_data):
        """Test date parsing from YYYY-MM-DD format."""
        valid_invoice_data["Fecha_emision"] = "2024-01-15"
        valid_invoice_data["Fecha_recepcion"] = "2024-01-16"

        invoice = CreateYiqiInvoiceCommand(**valid_invoice_data)

        assert invoice.Fecha_emision == date(2024, 1, 15)
        assert invoice.Fecha_recepcion == date(2024, 1, 16)

    def test_date_string_format_dd_mm_yyyy(self, valid_invoice_data):
        """Test date parsing from DD/MM/YYYY format."""
        valid_invoice_data["Fecha_emision"] = "15/01/2024"
        valid_invoice_data["Fecha_recepcion"] = "16/01/2024"

        invoice = CreateYiqiInvoiceCommand(**valid_invoice_data)

        assert invoice.Fecha_emision == date(2024, 1, 15)
        assert invoice.Fecha_recepcion == date(2024, 1, 16)

    def test_date_invalid_format(self, valid_invoice_data):
        """Test invalid date format raises error."""
        valid_invoice_data["Fecha_emision"] = "2024/15/01"  # Invalid

        with pytest.raises(ValueError, match="Invalid date format"):
            CreateYiqiInvoiceCommand(**valid_invoice_data)

    def test_emission_date_cannot_be_future(self, valid_invoice_data):
        """Test emission date cannot be in the future."""
        future_date = date.today() + timedelta(days=1)
        valid_invoice_data["Fecha_emision"] = future_date

        with pytest.raises(ValueError, match="cannot be in the future"):
            CreateYiqiInvoiceCommand(**valid_invoice_data)

    def test_reception_before_emission_fails(self, valid_invoice_data):
        """Test reception date cannot be before emission date."""
        valid_invoice_data["Fecha_emision"] = date(2024, 1, 15)
        valid_invoice_data["Fecha_recepcion"] = date(2024, 1, 10)

        with pytest.raises(ValueError, match="cannot be before"):
            CreateYiqiInvoiceCommand(**valid_invoice_data)

    def test_reception_same_as_emission_ok(self, valid_invoice_data):
        """Test reception date can be same as emission."""
        same_date = date(2024, 1, 15)
        valid_invoice_data["Fecha_emision"] = same_date
        valid_invoice_data["Fecha_recepcion"] = same_date

        invoice = CreateYiqiInvoiceCommand(**valid_invoice_data)

        assert invoice.Fecha_emision == invoice.Fecha_recepcion


# === Test AWB Validation ===

class TestAWBValidation:
    """Test Air Waybill validation."""

    def test_valid_awb_11_digits(self, valid_invoice_data):
        """Test valid 11-digit AWB."""
        valid_invoice_data["AWB"] = "123-45678901"

        invoice = CreateYiqiInvoiceCommand(**valid_invoice_data)

        assert invoice.AWB == "123-45678901"

    def test_valid_awb_8_digits(self, valid_invoice_data):
        """Test valid 8-digit AWB."""
        valid_invoice_data["AWB"] = "12345678"

        invoice = CreateYiqiInvoiceCommand(**valid_invoice_data)

        assert invoice.AWB == "12345678"

    def test_awb_with_letters_fails(self, valid_invoice_data):
        """Test AWB with letters fails validation."""
        valid_invoice_data["AWB"] = "ABC12345678"

        with pytest.raises(ValueError, match="must contain only digits and hyphens"):
            CreateYiqiInvoiceCommand(**valid_invoice_data)

    def test_awb_wrong_length_fails(self, valid_invoice_data):
        """Test AWB with wrong length fails."""
        valid_invoice_data["AWB"] = "123"  # Too short

        with pytest.raises(ValueError, match="must be 8 or 11 digits"):
            CreateYiqiInvoiceCommand(**valid_invoice_data)

    def test_awb_none_is_valid(self, valid_invoice_data):
        """Test AWB can be None (optional field)."""
        valid_invoice_data["AWB"] = None

        invoice = CreateYiqiInvoiceCommand(**valid_invoice_data)

        assert invoice.AWB is None


# === Test Weight and Items Validation ===

class TestWeightItemsValidation:
    """Test weight and items validation."""

    def test_weight_must_be_positive(self, valid_invoice_data):
        """Test weight must be positive."""
        valid_invoice_data["Kg"] = -10.5

        with pytest.raises(ValueError, match="cannot be negative"):
            CreateYiqiInvoiceCommand(**valid_invoice_data)

    def test_weight_unreasonably_high_fails(self, valid_invoice_data):
        """Test unreasonably high weight fails."""
        valid_invoice_data["Kg"] = 200000.0  # 200 tons

        with pytest.raises(ValueError, match="unreasonably high"):
            CreateYiqiInvoiceCommand(**valid_invoice_data)

    def test_items_must_be_positive(self, valid_invoice_data):
        """Test items must be positive."""
        valid_invoice_data["Items"] = 0

        with pytest.raises(ValueError, match="must be greater than 0"):
            CreateYiqiInvoiceCommand(**valid_invoice_data)

    def test_average_weight_too_low_fails(self, valid_invoice_data):
        """Test average weight per item validation."""
        valid_invoice_data["Kg"] = 0.0001
        valid_invoice_data["Items"] = 1000

        with pytest.raises(ValueError, match="Average weight per item too low"):
            CreateYiqiInvoiceCommand(**valid_invoice_data)

    def test_average_weight_too_high_fails(self, valid_invoice_data):
        """Test average weight per item too high fails."""
        valid_invoice_data["Kg"] = 10000.0
        valid_invoice_data["Items"] = 1

        with pytest.raises(ValueError, match="Average weight per item too high"):
            CreateYiqiInvoiceCommand(**valid_invoice_data)


# === Test Computed Fields ===

class TestComputedFields:
    """Test computed fields."""

    def test_days_to_reception(self, valid_invoice_data):
        """Test days_to_reception computed field."""
        valid_invoice_data["Fecha_emision"] = date(2024, 1, 15)
        valid_invoice_data["Fecha_recepcion"] = date(2024, 1, 18)

        invoice = CreateYiqiInvoiceCommand(**valid_invoice_data)

        assert invoice.days_to_reception == 3

    def test_days_to_reception_same_day(self, valid_invoice_data):
        """Test days_to_reception when same day."""
        same_date = date(2024, 1, 15)
        valid_invoice_data["Fecha_emision"] = same_date
        valid_invoice_data["Fecha_recepcion"] = same_date

        invoice = CreateYiqiInvoiceCommand(**valid_invoice_data)

        assert invoice.days_to_reception == 0

    def test_is_same_month_service_true(self, valid_invoice_data):
        """Test is_same_month_service when true."""
        valid_invoice_data["Fecha_emision"] = date(2024, 1, 15)
        valid_invoice_data["Mes_servicio"] = date(2024, 1, 1)

        invoice = CreateYiqiInvoiceCommand(**valid_invoice_data)

        assert invoice.is_same_month_service is True

    def test_is_same_month_service_false(self, valid_invoice_data):
        """Test is_same_month_service when false."""
        valid_invoice_data["Fecha_emision"] = date(2024, 1, 15)
        valid_invoice_data["Mes_servicio"] = date(2024, 2, 1)

        invoice = CreateYiqiInvoiceCommand(**valid_invoice_data)

        assert invoice.is_same_month_service is False

    def test_average_weight_per_item(self, valid_invoice_data):
        """Test average_weight_per_item computed field."""
        valid_invoice_data["Kg"] = 100.0
        valid_invoice_data["Items"] = 10

        invoice = CreateYiqiInvoiceCommand(**valid_invoice_data)

        assert invoice.average_weight_per_item == 10.0

    def test_average_weight_none_when_missing(self, valid_invoice_data):
        """Test average_weight_per_item is None when data missing."""
        # Don't set Kg and Items

        invoice = CreateYiqiInvoiceCommand(**valid_invoice_data)

        assert invoice.average_weight_per_item is None


# === Test Serialization ===

class TestSerialization:
    """Test field serialization."""

    def test_date_serialization_format(self, valid_invoice_data):
        """Test dates are serialized to DD/MM/YYYY format."""
        invoice = CreateYiqiInvoiceCommand(**valid_invoice_data)

        # Serialize to dict with aliases
        data = invoice.model_dump(by_alias=True)

        # Dates should be in DD/MM/YYYY format
        assert data["2881"] == "15/01/2024"  # Fecha_emision
        assert data["5112"] == "16/01/2024"  # Fecha_recepcion
        assert data["5082"] == "01/01/2024"  # Mes_servicio

    def test_decimal_serialization(self, valid_invoice_data):
        """Test Decimal is serialized to float."""
        invoice = CreateYiqiInvoiceCommand(**valid_invoice_data)

        data = invoice.model_dump(by_alias=True)

        # Precio_unitario should be float, not Decimal
        assert isinstance(data["6405"], float)
        assert data["6405"] == 1500.50


# === Test UploadFileCommand ===

class TestUploadFileCommand:
    """Test file upload command."""

    def test_create_upload_command(self):
        """Test creating upload command."""
        file_content = b"test file content"
        file = BytesIO(file_content)

        cmd = UploadFileCommand(
            file=file,
            size=len(file_content),
            filename="test.pdf"
        )

        assert cmd.size == len(file_content)
        assert cmd.filename == "test.pdf"

    def test_file_too_large_fails(self):
        """Test file size validation."""
        file = BytesIO(b"x" * (11 * 1024 * 1024))  # 11 MB

        with pytest.raises(ValueError, match="File too large"):
            UploadFileCommand(
                file=file,
                size=11 * 1024 * 1024,
                filename="large.pdf"
            )

    def test_file_too_small_fails(self):
        """Test minimum file size."""
        with pytest.raises(ValueError, match="File too small"):
            UploadFileCommand(
                file=BytesIO(b""),
                size=0,
                filename="empty.pdf"
            )

    def test_filename_without_extension_fails(self):
        """Test filename must have extension."""
        with pytest.raises(ValueError, match="must have an extension"):
            UploadFileCommand(
                file=BytesIO(b"test"),
                size=4,
                filename="noextension"
            )

    def test_filename_with_invalid_chars_fails(self):
        """Test filename validation for invalid characters."""
        with pytest.raises(ValueError, match="invalid characters"):
            UploadFileCommand(
                file=BytesIO(b"test"),
                size=4,
                filename="file@#$.pdf"
            )


# === Test Model Config ===

class TestModelConfig:
    """Test model configuration behaviors."""

    def test_extra_fields_forbidden(self, valid_invoice_data):
        """Test extra fields are rejected."""
        valid_invoice_data["unknown_field"] = "value"

        with pytest.raises(ValueError, match="Extra inputs are not permitted"):
            CreateYiqiInvoiceCommand(**valid_invoice_data)

    def test_whitespace_stripped(self, valid_invoice_data):
        """Test whitespace is automatically stripped."""
        valid_invoice_data["Numero"] = "  001-001-0001  "
        valid_invoice_data["Concepto"] = "  Test concept  "

        invoice = CreateYiqiInvoiceCommand(**valid_invoice_data)

        assert invoice.Numero == "001-001-0001"
        assert invoice.Concepto == "Test concept"

    def test_populate_by_name(self, valid_invoice_data):
        """Test can use field name instead of alias."""
        # Use field name instead of alias
        data_with_names = {
            "Provider": 123,
            "Numero": "001-001-0001",
            "Concepto": "Test",
            "Fecha_emision": date(2024, 1, 15),
            "Fecha_recepcion": date(2024, 1, 16),
            "Mes_servicio": date(2024, 1, 1),
            "Precio_unitario": Decimal("100.0"),
        }

        invoice = CreateYiqiInvoiceCommand(**data_with_names)

        assert invoice.Provider == 123


# === Test JSON Schema Generation ===

class TestJSONSchema:
    """Test JSON schema generation."""

    def test_schema_includes_descriptions(self):
        """Test schema includes field descriptions."""
        schema = CreateYiqiInvoiceCommand.model_json_schema()

        assert "Provider" in schema["properties"]
        assert "description" in schema["properties"]["Provider"]

    def test_schema_includes_examples(self):
        """Test schema includes examples."""
        schema = CreateYiqiInvoiceCommand.model_json_schema()

        numero_schema = schema["properties"]["Numero"]
        assert "examples" in numero_schema
        assert len(numero_schema["examples"]) > 0


# === Integration Tests ===

class TestIntegration:
    """Integration tests with realistic scenarios."""

    def test_complete_invoice_with_all_fields(self):
        """Test creating invoice with all possible fields."""
        invoice = CreateYiqiInvoiceCommand(
            Provider=123,
            Numero="001-001-0000001",
            Concepto="Servicios de transporte aéreo internacional",
            Fecha_emision=date(2024, 1, 15),
            Fecha_recepcion=date(2024, 1, 16),
            Mes_servicio=date(2024, 1, 1),
            Precio_unitario=Decimal("1500.50"),
            Moneda_original=2,
            Servicio=456,
            AWB="123-45678901",
            Kg=50.5,
            Items=10,
            creado_en_portal=True
        )

        # Validate all fields
        assert invoice.Provider == 123
        assert invoice.Numero == "001-001-0000001"

        # Validate computed fields
        assert invoice.days_to_reception == 1
        assert invoice.average_weight_per_item == 5.05
        assert invoice.is_same_month_service is True

    def test_minimal_invoice(self):
        """Test creating invoice with minimal required fields."""
        invoice = CreateYiqiInvoiceCommand(
            Provider=123,
            Numero="001-001-0001",
            Concepto="Test invoice",
            Fecha_emision=date(2024, 1, 15),
            Fecha_recepcion=date(2024, 1, 15),
            Mes_servicio=date(2024, 1, 1),
            Precio_unitario=Decimal("100.0"),
        )

        assert invoice.Provider == 123
        assert invoice.AWB is None
        assert invoice.Kg is None
        assert invoice.Items is None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
