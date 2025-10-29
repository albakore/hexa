"""
Improved Commands for YiqiERP using Pydantic v2 best practices.

Key improvements:
1. ConfigDict for better configuration
2. Annotated types for reusable constraints
3. Better validators with clear error messages
4. Separation of concerns with mixins
5. Model validators for cross-field validation
6. Computed fields for derived values
7. Custom serializers for complex types
"""

from datetime import date, datetime
from decimal import Decimal
from io import BytesIO
from typing import Annotated, Optional, Any

from fastapi import File, UploadFile
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_serializer,
    field_validator,
    model_validator,
    computed_field,
)


# === Type Aliases with Constraints ===

PositiveInt = Annotated[int, Field(gt=0, description="Must be a positive integer")]

PositiveFloat = Annotated[
    float, Field(gt=0, description="Must be a positive number")
]

PositiveDecimal = Annotated[
    Decimal,
    Field(gt=0, decimal_places=4, description="Must be a positive decimal")
]

NonEmptyStr = Annotated[
    str,
    Field(min_length=1, max_length=500, description="Cannot be empty")
]

AWBString = Annotated[
    str,
    Field(
        min_length=1,
        max_length=50,
        pattern=r"^[0-9\-]+$",
        description="Air Waybill number (digits and hyphens only)"
    )
]

YiqiFieldId = Annotated[
    int,
    Field(gt=0, description="Yiqi field ID reference")
]


# === Helper Functions for Validation ===

def validate_date_not_future(v: date, field_name: str) -> date:
    """Ensure date is not in the future."""
    if v > date.today():
        raise ValueError(
            f"{field_name} cannot be in the future. Got: {v}"
        )
    return v


def validate_date_not_too_old(v: date, field_name: str, max_years: int = 10) -> date:
    """Ensure date is not too old."""
    from datetime import timedelta
    max_date = date.today() - timedelta(days=365 * max_years)
    if v < max_date:
        raise ValueError(
            f"{field_name} cannot be older than {max_years} years. Got: {v}"
        )
    return v


# === Base Invoice Model ===

class YiqiInvoiceBase(BaseModel):
    """
    Base model for Yiqi Invoice with core fields and validation.

    This model includes all required and optional fields with proper
    validation, serialization aliases, and constraints.
    """

    model_config = ConfigDict(
        # Validation settings
        validate_assignment=True,        # Validate on attribute changes
        validate_default=True,           # Validate default values
        strict=False,                    # Allow type coercion

        # Serialization settings
        populate_by_name=True,           # Allow both alias and field name
        use_enum_values=True,            # Use enum values not enum objects

        # Extra fields handling
        extra="forbid",                  # Reject unknown fields

        # String handling
        str_strip_whitespace=True,       # Auto-strip whitespace
        str_min_length=0,                # Min string length

        # JSON schema
        json_schema_extra={
            "title": "Yiqi Invoice",
            "description": "Command for creating an invoice in Yiqi ERP system"
        }
    )

    # === Required Fields ===

    Provider: PositiveInt = Field(
        serialization_alias="2880",
        description="Proveedor - ID del provider en Yiqi",
        examples=[123, 456]
    )

    Numero: NonEmptyStr = Field(
        serialization_alias="2879",
        description="Número de factura",
        examples=["001-001-0000001", "FAC-2024-001"]
    )

    Concepto: NonEmptyStr = Field(
        serialization_alias="2888",
        description="Concepto - descripción de la factura",
        examples=["Servicios de logística", "Transporte aéreo"]
    )

    Fecha_emision: date = Field(
        serialization_alias="2881",
        description="Fecha de emisión de la factura"
    )

    Fecha_recepcion: date = Field(
        serialization_alias="5112",
        description="Fecha de recepción de la factura"
    )

    Mes_servicio: date = Field(
        serialization_alias="5082",
        description="Mes del servicio facturado"
    )

    Precio_unitario: PositiveDecimal = Field(
        serialization_alias="6405",
        description="Precio unitario del servicio",
        examples=[100.50, 1500.75]
    )

    # === Optional Fields ===

    AWB: Optional[AWBString] = Field(
        default=None,
        serialization_alias="7102",
        description="Air Waybill number",
        examples=["123-45678901", "98765432101"]
    )

    Servicio: Optional[YiqiFieldId] = Field(
        default=None,
        serialization_alias="6196",
        description="ID del servicio en Yiqi"
    )

    Moneda_original: Optional[YiqiFieldId] = Field(
        default=None,
        serialization_alias="5074",
        description="ID de la moneda en Yiqi",
        examples=[1, 2, 3]  # 1=ARS, 2=USD, etc.
    )

    Kg: Optional[PositiveFloat] = Field(
        default=None,
        serialization_alias="6599",
        description="Kilogramos del envío",
        examples=[10.5, 100.25],
        ge=0  # Greater or equal to 0
    )

    Items: Optional[PositiveInt] = Field(
        default=None,
        serialization_alias="6600",
        description="Cantidad de items",
        examples=[1, 10, 100]
    )

    creado_en_portal: Optional[bool] = Field(
        default=False,
        serialization_alias="7677",
        description="Indica si fue creado desde el portal"
    )

    # === Field Validators ===

    @field_validator("Numero")
    @classmethod
    def validate_numero_format(cls, v: str) -> str:
        """
        Validate invoice number format.

        Common formats:
        - 001-001-0000001
        - FAC-2024-001
        """
        v = v.strip().upper()

        if not v:
            raise ValueError("Invoice number cannot be empty")

        # Check for minimum length
        if len(v) < 3:
            raise ValueError(
                f"Invoice number too short: {v}. "
                "Minimum 3 characters required."
            )

        return v

    @field_validator("Concepto")
    @classmethod
    def validate_concepto(cls, v: str) -> str:
        """Validate concept field."""
        v = v.strip()

        if not v:
            raise ValueError("Concepto cannot be empty")

        if len(v) < 5:
            raise ValueError(
                f"Concepto too short: '{v}'. "
                "Minimum 5 characters for meaningful description."
            )

        return v

    @field_validator("Fecha_emision", "Fecha_recepcion", mode="before")
    @classmethod
    def validate_dates(cls, v: Any) -> date:
        """
        Validate and parse dates.

        Accepts: date, datetime, or string in various formats.
        """
        if isinstance(v, date):
            return v

        if isinstance(v, datetime):
            return v.date()

        if isinstance(v, str):
            # Try parsing common date formats
            for fmt in ["%Y-%m-%d", "%d/%m/%Y", "%Y/%m/%d"]:
                try:
                    return datetime.strptime(v, fmt).date()
                except ValueError:
                    continue

            raise ValueError(
                f"Invalid date format: {v}. "
                "Expected: YYYY-MM-DD or DD/MM/YYYY"
            )

        raise ValueError(f"Invalid date type: {type(v)}")

    @field_validator("AWB")
    @classmethod
    def validate_awb(cls, v: Optional[str]) -> Optional[str]:
        """Validate Air Waybill number format."""
        if v is None:
            return v

        v = v.strip()

        # Remove hyphens for validation
        awb_digits = v.replace("-", "")

        if not awb_digits.isdigit():
            raise ValueError(
                f"AWB must contain only digits and hyphens: {v}"
            )

        # AWB typically has 11 digits
        if len(awb_digits) not in [8, 11]:
            raise ValueError(
                f"AWB must be 8 or 11 digits long: {v} "
                f"(got {len(awb_digits)} digits)"
            )

        return v

    @field_validator("Kg")
    @classmethod
    def validate_weight(cls, v: Optional[float]) -> Optional[float]:
        """Validate weight is reasonable."""
        if v is None:
            return v

        if v < 0:
            raise ValueError(f"Weight cannot be negative: {v}")

        # Reasonable max weight for air cargo (in kg)
        MAX_WEIGHT = 100000  # 100 tons
        if v > MAX_WEIGHT:
            raise ValueError(
                f"Weight seems unreasonably high: {v} kg. "
                f"Maximum allowed: {MAX_WEIGHT} kg"
            )

        return v

    @field_validator("Items")
    @classmethod
    def validate_items(cls, v: Optional[int]) -> Optional[int]:
        """Validate item count is reasonable."""
        if v is None:
            return v

        if v <= 0:
            raise ValueError(f"Items must be greater than 0: {v}")

        MAX_ITEMS = 100000
        if v > MAX_ITEMS:
            raise ValueError(
                f"Item count seems unreasonably high: {v}. "
                f"Maximum allowed: {MAX_ITEMS}"
            )

        return v

    # === Model Validators (cross-field validation) ===

    @model_validator(mode="after")
    def validate_date_relationships(self) -> "YiqiInvoiceBase":
        """
        Validate relationships between dates.

        Rules:
        1. Fecha_recepcion >= Fecha_emision
        2. Mes_servicio should be close to Fecha_emision
        3. No dates in the future
        """
        # Check emission date not in future
        if self.Fecha_emision > date.today():
            raise ValueError(
                f"Emission date cannot be in the future: {self.Fecha_emision}"
            )

        # Check reception date not before emission date
        if self.Fecha_recepcion < self.Fecha_emision:
            raise ValueError(
                f"Reception date ({self.Fecha_recepcion}) cannot be "
                f"before emission date ({self.Fecha_emision})"
            )

        # Check reception date not too far in the future
        from datetime import timedelta
        max_reception = date.today() + timedelta(days=30)
        if self.Fecha_recepcion > max_reception:
            raise ValueError(
                f"Reception date ({self.Fecha_recepcion}) seems too far "
                f"in the future (max: {max_reception})"
            )

        # Warn if service month is very different from emission
        # (could be intentional, so we don't raise, just validate range)
        service_year_diff = abs(
            self.Mes_servicio.year - self.Fecha_emision.year
        )
        if service_year_diff > 2:
            # Could log warning here if logging is available
            pass

        return self

    @model_validator(mode="after")
    def validate_weight_and_items(self) -> "YiqiInvoiceBase":
        """
        Validate weight and items make sense together.

        If both are provided, check they're proportional.
        """
        if self.Kg is not None and self.Items is not None:
            # Average weight per item
            avg_weight = self.Kg / self.Items

            # Sanity check: average weight should be reasonable
            # (between 0.001 kg and 1000 kg per item)
            if avg_weight < 0.001:
                raise ValueError(
                    f"Average weight per item too low: {avg_weight:.4f} kg/item. "
                    f"Total: {self.Kg} kg, Items: {self.Items}"
                )

            if avg_weight > 1000:
                raise ValueError(
                    f"Average weight per item too high: {avg_weight:.2f} kg/item. "
                    f"Total: {self.Kg} kg, Items: {self.Items}"
                )

        return self

    # === Computed Fields ===

    @computed_field  # type: ignore[misc]
    @property
    def days_to_reception(self) -> int:
        """Calculate days between emission and reception."""
        return (self.Fecha_recepcion - self.Fecha_emision).days

    @computed_field  # type: ignore[misc]
    @property
    def is_same_month_service(self) -> bool:
        """Check if service month matches emission month."""
        return (
            self.Mes_servicio.year == self.Fecha_emision.year and
            self.Mes_servicio.month == self.Fecha_emision.month
        )

    @computed_field  # type: ignore[misc]
    @property
    def average_weight_per_item(self) -> Optional[float]:
        """Calculate average weight per item if both are available."""
        if self.Kg is not None and self.Items is not None and self.Items > 0:
            return round(self.Kg / self.Items, 4)
        return None

    # === Field Serializers ===

    @field_serializer("Fecha_emision", "Fecha_recepcion", "Mes_servicio")
    def serialize_dates(self, v: date) -> str:
        """
        Serialize dates to Yiqi format: DD/MM/YYYY.

        This replaces the old field_validator approach.
        """
        return v.strftime("%d/%m/%Y")

    @field_serializer("Precio_unitario")
    def serialize_price(self, v: Decimal) -> float:
        """Serialize Decimal to float for JSON."""
        return float(v)


# === File Attachments Model ===

class YiqiInvoiceAttachments(BaseModel):
    """
    Separate model for file attachments.

    Keeps file handling logic separate from invoice data.
    """

    model_config = ConfigDict(
        extra="forbid",
        arbitrary_types_allowed=True,  # Allow UploadFile
    )

    Comprobante: Optional[UploadFile] = Field(
        default=None,
        serialization_alias="2891",
        description="Archivo comprobante (PDF, imagen, etc.)"
    )

    Detalle: Optional[UploadFile] = Field(
        default=None,
        serialization_alias="5494",
        description="Archivo con detalle adicional"
    )

    @field_validator("Comprobante", "Detalle")
    @classmethod
    def validate_file_size(cls, v: Optional[UploadFile]) -> Optional[UploadFile]:
        """Validate uploaded file size."""
        if v is None:
            return v

        # Check if file has size attribute
        if hasattr(v, "size") and v.size is not None:
            MAX_SIZE = 10 * 1024 * 1024  # 10 MB
            if v.size > MAX_SIZE:
                raise ValueError(
                    f"File too large: {v.size / 1024 / 1024:.2f} MB. "
                    f"Maximum: {MAX_SIZE / 1024 / 1024} MB"
                )

        # Validate filename exists
        if hasattr(v, "filename") and not v.filename:
            raise ValueError("File must have a filename")

        return v

    @field_serializer("Comprobante", "Detalle")
    def serialize_file(self, v: Optional[UploadFile]) -> Optional[str]:
        """
        Serialize file to filename only.

        This is what gets sent to Yiqi after upload.
        """
        if v is None:
            return None

        if hasattr(v, "filename"):
            return v.filename

        return None


# === Combined Command ===

class CreateYiqiInvoiceCommand(YiqiInvoiceBase, YiqiInvoiceAttachments):
    """
    Complete command for creating a Yiqi Invoice.

    Combines invoice data and file attachments with full validation.

    Example:
        >>> cmd = CreateYiqiInvoiceCommand(
        ...     Provider=123,
        ...     Numero="001-001-0001",
        ...     Concepto="Servicios de transporte",
        ...     Fecha_emision=date(2024, 1, 15),
        ...     Fecha_recepcion=date(2024, 1, 16),
        ...     Mes_servicio=date(2024, 1, 1),
        ...     Precio_unitario=Decimal("1500.50"),
        ...     AWB="123-45678901",
        ...     Kg=50.5,
        ...     Items=10
        ... )
    """
    # Inherits model_config from parent classes


# === Upload File Command ===

class UploadFileCommand(BaseModel):
    """
    Command for uploading a file to Yiqi.

    Wraps file data with metadata for upload.
    """

    model_config = ConfigDict(
        arbitrary_types_allowed=True
    )

    file: BytesIO = Field(
        description="File content as BytesIO stream"
    )

    size: PositiveInt = Field(
        description="File size in bytes"
    )

    filename: NonEmptyStr = Field(
        description="Original filename with extension"
    )

    @field_validator("size")
    @classmethod
    def validate_size(cls, v: int) -> int:
        """Validate file size is reasonable."""
        MAX_SIZE = 10 * 1024 * 1024  # 10 MB
        if v > MAX_SIZE:
            raise ValueError(
                f"File too large: {v / 1024 / 1024:.2f} MB. "
                f"Maximum: {MAX_SIZE / 1024 / 1024} MB"
            )

        MIN_SIZE = 1  # At least 1 byte
        if v < MIN_SIZE:
            raise ValueError(f"File too small: {v} bytes")

        return v

    @field_validator("filename")
    @classmethod
    def validate_filename(cls, v: str) -> str:
        """Validate filename format."""
        v = v.strip()

        if not v:
            raise ValueError("Filename cannot be empty")

        # Check for file extension
        if "." not in v:
            raise ValueError(
                f"Filename must have an extension: {v}"
            )

        # Check for valid characters (basic validation)
        import re
        if not re.match(r'^[a-zA-Z0-9_\-. ]+$', v):
            raise ValueError(
                f"Filename contains invalid characters: {v}. "
                "Allowed: letters, numbers, spaces, -, _, ."
            )

        return v

    def __init__(
        self,
        file: BytesIO,
        size: int,
        filename: str,
        **data
    ):
        """Custom constructor for easier instantiation."""
        super().__init__(file=file, size=size, filename=filename, **data)
