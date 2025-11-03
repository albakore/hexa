# Guía de Migración a Pydantic v2 - Comandos YiqiERP

## Resumen de Mejoras

Esta guía documenta las mejoras implementadas al migrar los comandos de YiqiERP a Pydantic v2, haciendo el código más legible, mantenible y robusto.

---

## 🎯 Principales Mejoras

### 1. **ConfigDict en lugar de dict literal**

**Antes:**
```python
model_config = {"extra": "forbid"}
```

**Después:**
```python
from pydantic import ConfigDict

model_config = ConfigDict(
    validate_assignment=True,    # Valida al asignar valores
    validate_default=True,        # Valida valores por defecto
    extra="forbid",               # Rechaza campos desconocidos
    str_strip_whitespace=True,    # Limpia espacios automáticamente
    populate_by_name=True,        # Permite usar alias o nombre
)
```

**Beneficios:**
- Autocompletado en IDE
- Type checking
- Documentación integrada
- Más opciones de configuración

---

### 2. **Annotated Types para Reutilización**

**Antes:**
```python
Provider: int = Field(serialization_alias="2880")
Servicio: Optional[int] = Field(serialization_alias="6196")
```

**Después:**
```python
from typing import Annotated

PositiveInt = Annotated[int, Field(gt=0, description="Must be positive")]

Provider: PositiveInt = Field(
    serialization_alias="2880",
    description="Proveedor - ID del provider en Yiqi",
    examples=[123, 456]
)

Servicio: Optional[PositiveInt] = Field(
    default=None,
    serialization_alias="6196",
    description="ID del servicio en Yiqi"
)
```

**Beneficios:**
- Reutilización de constraints
- Código más DRY
- Validaciones consistentes
- Mejor documentación

---

### 3. **Field Validators Mejorados**

**Antes:**
```python
@field_validator("Fecha_emision", "Fecha_recepcion", "Mes_servicio", mode="after")
def parse_dob(cls, v):
    return date.strftime(v, "%d/%m/%Y")
```

**Problemas:**
- Nombre confuso (`parse_dob` para fechas de factura)
- Sin validación de datos
- Mezcla validación con serialización

**Después:**
```python
# Validación
@field_validator("Fecha_emision", "Fecha_recepcion", mode="before")
@classmethod
def validate_dates(cls, v: Any) -> date:
    """
    Validate and parse dates.

    Accepts: date, datetime, or string in various formats.
    """
    if isinstance(v, date):
        return v

    if isinstance(v, str):
        for fmt in ["%Y-%m-%d", "%d/%m/%Y"]:
            try:
                return datetime.strptime(v, fmt).date()
            except ValueError:
                continue

        raise ValueError(f"Invalid date format: {v}")

    raise ValueError(f"Invalid date type: {type(v)}")

# Serialización (separada)
@field_serializer("Fecha_emision", "Fecha_recepcion", "Mes_servicio")
def serialize_dates(self, v: date) -> str:
    """Serialize dates to Yiqi format: DD/MM/YYYY."""
    return v.strftime("%d/%m/%Y")
```

**Beneficios:**
- Separación de responsabilidades
- Nombres descriptivos
- Documentación clara
- Mejor manejo de errores
- Type hints correctos

---

### 4. **Model Validators para Validación Cross-Field**

**Nuevo:**
```python
@model_validator(mode="after")
def validate_date_relationships(self) -> "YiqiInvoiceBase":
    """
    Validate relationships between dates.

    Rules:
    1. Fecha_recepcion >= Fecha_emision
    2. No dates in the future
    """
    if self.Fecha_recepcion < self.Fecha_emision:
        raise ValueError(
            f"Reception date ({self.Fecha_recepcion}) cannot be "
            f"before emission date ({self.Fecha_emision})"
        )

    if self.Fecha_emision > date.today():
        raise ValueError(
            f"Emission date cannot be in the future: {self.Fecha_emision}"
        )

    return self
```

**Beneficios:**
- Validación de relaciones entre campos
- Lógica de negocio en el modelo
- Errores claros y específicos

---

### 5. **Computed Fields para Valores Derivados**

**Nuevo:**
```python
@computed_field
@property
def days_to_reception(self) -> int:
    """Calculate days between emission and reception."""
    return (self.Fecha_recepcion - self.Fecha_emision).days

@computed_field
@property
def average_weight_per_item(self) -> Optional[float]:
    """Calculate average weight per item."""
    if self.Kg is not None and self.Items is not None and self.Items > 0:
        return round(self.Kg / self.Items, 4)
    return None
```

**Beneficios:**
- Cálculos automáticos
- No duplicar lógica
- Valores siempre consistentes
- Se incluyen en serialización

---

### 6. **Validaciones Específicas con Mensajes Claros**

**Antes:**
```python
# Sin validación específica
AWB: Optional[str] = Field(serialization_alias="7102")
```

**Después:**
```python
AWBString = Annotated[
    str,
    Field(
        min_length=1,
        max_length=50,
        pattern=r"^[0-9\-]+$",
        description="Air Waybill (digits and hyphens only)"
    )
]

AWB: Optional[AWBString] = Field(
    default=None,
    serialization_alias="7102",
    description="Air Waybill number",
    examples=["123-45678901"]
)

@field_validator("AWB")
@classmethod
def validate_awb(cls, v: Optional[str]) -> Optional[str]:
    """Validate Air Waybill format."""
    if v is None:
        return v

    v = v.strip()
    awb_digits = v.replace("-", "")

    if not awb_digits.isdigit():
        raise ValueError(f"AWB must contain only digits and hyphens: {v}")

    if len(awb_digits) not in [8, 11]:
        raise ValueError(
            f"AWB must be 8 or 11 digits: {v} (got {len(awb_digits)})"
        )

    return v
```

**Beneficios:**
- Validación de formato específico
- Mensajes de error útiles
- Documentación del formato esperado

---

### 7. **Separación de Responsabilidades**

**Antes:**
```python
class CreateYiqiInvoiceCommand(YiqiInvoice, YiqiInvoiceAttach):
    ...
```

**Después:**
```python
class YiqiInvoiceBase(BaseModel, DateValidatorMixin):
    """Core invoice data with validation."""
    # ... campos y validaciones de datos

class YiqiInvoiceAttachments(BaseModel):
    """File attachments with separate validation."""
    # ... campos y validaciones de archivos

class CreateYiqiInvoiceCommand(YiqiInvoiceBase, YiqiInvoiceAttachments):
    """Complete command combining data and files."""
    pass
```

**Beneficios:**
- Cada clase tiene una responsabilidad clara
- Fácil de testear por separado
- Reutilizable en otros contextos

---

### 8. **Mixins para Lógica Reutilizable**

**Nuevo:**
```python
class DateValidatorMixin(BaseModel):
    """Reusable date validation logic."""

    @staticmethod
    def validate_date_not_future(v: date, field_name: str) -> date:
        """Ensure date is not in the future."""
        if v > date.today():
            raise ValueError(
                f"{field_name} cannot be in the future. Got: {v}"
            )
        return v
```

**Beneficios:**
- Lógica compartida
- Fácil de testear
- Reutilizable en otros modelos

---

## 📊 Comparación de Legibilidad

### Ejemplo: Campo con validación

**Antes:**
```python
Precio_unitario: int | float = Field(serialization_alias="6405")
```

**Después:**
```python
Precio_unitario: PositiveDecimal = Field(
    serialization_alias="6405",
    description="Precio unitario del servicio",
    examples=[100.50, 1500.75]
)
```

**Mejoras:**
- ✅ Tipo más específico (Decimal en lugar de int|float)
- ✅ Constraint incluido (debe ser positivo)
- ✅ Descripción clara
- ✅ Ejemplos para documentación

---

## 🔄 Cómo Migrar

### Paso 1: Reemplazar imports

```python
# Antes
from pydantic import BaseModel, Field, field_serializer, field_validator

# Después
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_serializer,
    field_validator,
    model_validator,
    computed_field,
)
```

### Paso 2: Actualizar model_config

```python
# Antes
model_config = {"extra": "forbid"}

# Después
model_config = ConfigDict(
    validate_assignment=True,
    extra="forbid",
    str_strip_whitespace=True,
    populate_by_name=True,
)
```

### Paso 3: Crear Annotated types

```python
PositiveInt = Annotated[int, Field(gt=0, description="Must be positive")]
NonEmptyStr = Annotated[str, Field(min_length=1, max_length=500)]
```

### Paso 4: Agregar validaciones

```python
@field_validator("campo")
@classmethod
def validate_campo(cls, v: str) -> str:
    """Validate field with clear error messages."""
    if not v.strip():
        raise ValueError("Field cannot be empty")
    return v.strip()
```

### Paso 5: Separar validación y serialización

```python
# Validación
@field_validator("fecha", mode="before")
@classmethod
def validate_fecha(cls, v: Any) -> date:
    # ... parse and validate

# Serialización
@field_serializer("fecha")
def serialize_fecha(self, v: date) -> str:
    return v.strftime("%d/%m/%Y")
```

---

## 🧪 Testing

Con las mejoras, los tests son más fáciles:

```python
def test_invoice_validation():
    # Test fecha futura (debe fallar)
    with pytest.raises(ValueError, match="cannot be in the future"):
        CreateYiqiInvoiceCommand(
            Fecha_emision=date.today() + timedelta(days=1),
            # ... otros campos
        )

    # Test AWB inválido
    with pytest.raises(ValueError, match="AWB must be 8 or 11 digits"):
        CreateYiqiInvoiceCommand(
            AWB="123",  # Muy corto
            # ... otros campos
        )

    # Test relación de fechas
    with pytest.raises(ValueError, match="Reception date.*cannot be before"):
        CreateYiqiInvoiceCommand(
            Fecha_emision=date(2024, 1, 15),
            Fecha_recepcion=date(2024, 1, 10),  # Antes de emisión
            # ... otros campos
        )
```

---

## 📈 Beneficios Medibles

| Aspecto | Antes | Después | Mejora |
|---------|-------|---------|--------|
| Líneas de código | ~74 | ~550 | +642% (más validación) |
| Validaciones | 1 | 15+ | +1400% |
| Documentación | Mínima | Completa | ✅ |
| Type safety | Básico | Completo | ✅ |
| Mensajes de error | Genéricos | Específicos | ✅ |
| Testabilidad | Media | Alta | ✅ |

---

## 🎓 Conceptos Clave de Pydantic v2

### 1. **Validators vs Serializers**
- **Validators**: Transforman y validan INPUT (antes de crear el objeto)
- **Serializers**: Transforman OUTPUT (al exportar/serializar)

### 2. **Mode "before" vs "after"**
- **before**: Se ejecuta antes de la conversión de tipo de Pydantic
- **after**: Se ejecuta después de la conversión de tipo

### 3. **Field vs Annotated**
- **Field**: Para una sola instancia
- **Annotated**: Para reutilizar en múltiples campos

### 4. **Model Config**
- Centraliza configuración del modelo
- Mejor que decoradores/variables dispersas

---

## 🚀 Próximos Pasos

1. **Actualizar task** en `yiqi_erp.py` para usar el nuevo comando
2. **Migrar tests** para validar nuevas funcionalidades
3. **Documentar** casos de uso específicos
4. **Considerar** crear más comandos con este patrón

---

## 📚 Referencias

- [Pydantic v2 Documentation](https://docs.pydantic.dev/latest/)
- [Field Validators](https://docs.pydantic.dev/latest/concepts/validators/)
- [Model Validators](https://docs.pydantic.dev/latest/concepts/validators/#model-validators)
- [Computed Fields](https://docs.pydantic.dev/latest/concepts/computed_fields/)
- [Serialization](https://docs.pydantic.dev/latest/concepts/serialization/)
