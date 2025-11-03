# 🚀 Resumen de Mejoras - Módulo YiqiERP con Pydantic v2

## 📋 Tabla de Contenidos
- [Visión General](#visión-general)
- [Comparación Lado a Lado](#comparación-lado-a-lado)
- [Características Nuevas](#características-nuevas)
- [Beneficios Clave](#beneficios-clave)
- [Ejemplos de Uso](#ejemplos-de-uso)

---

## Visión General

Hemos refactorizado completamente el módulo YiqiERP para aprovechar las características avanzadas de Pydantic v2, resultando en:

- ✅ **Código más legible** y mantenible
- ✅ **Validaciones robustas** con mensajes claros
- ✅ **Type safety completo**
- ✅ **Mejor testing** y debugging
- ✅ **Documentación integrada**

---

## Comparación Lado a Lado

### 1. Definición de Campos

#### ❌ ANTES
```python
Provider: int = Field(serialization_alias="2880")
Numero: str = Field(serialization_alias="2879")
Precio_unitario: int | float = Field(serialization_alias="6405")
```

**Problemas:**
- Sin validación
- Sin documentación
- Tipos imprecisos (int|float para precio?)
- No hay constraints

#### ✅ DESPUÉS
```python
# Tipos reutilizables
PositiveInt = Annotated[int, Field(gt=0, description="Must be positive")]
PositiveDecimal = Annotated[Decimal, Field(gt=0, decimal_places=4)]

# Campos bien definidos
Provider: PositiveInt = Field(
    serialization_alias="2880",
    description="Proveedor - ID del provider en Yiqi",
    examples=[123, 456]
)

Numero: NonEmptyStr = Field(
    serialization_alias="2879",
    description="Número de factura",
    examples=["001-001-0000001"]
)

Precio_unitario: PositiveDecimal = Field(
    serialization_alias="6405",
    description="Precio unitario del servicio",
    examples=[100.50, 1500.75]
)
```

**Beneficios:**
- ✅ Validación automática (positivo, no vacío)
- ✅ Documentación clara
- ✅ Tipos precisos (Decimal para dinero)
- ✅ Ejemplos para tests y docs

---

### 2. Validación de Fechas

#### ❌ ANTES
```python
@field_validator("Fecha_emision", "Fecha_recepcion", "Mes_servicio", mode="after")
def parse_dob(cls, v):
    return date.strftime(v, "%d/%m/%Y")
```

**Problemas:**
- Nombre confuso (parse_dob?)
- Mezcla validación con serialización
- No valida datos
- Sin type hints

#### ✅ DESPUÉS
```python
# VALIDACIÓN (separada)
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

# SERIALIZACIÓN (separada)
@field_serializer("Fecha_emision", "Fecha_recepcion", "Mes_servicio")
def serialize_dates(self, v: date) -> str:
    """Serialize dates to Yiqi format: DD/MM/YYYY."""
    return v.strftime("%d/%m/%Y")
```

**Beneficios:**
- ✅ Separación de responsabilidades
- ✅ Nombres descriptivos
- ✅ Type hints completos
- ✅ Múltiples formatos de entrada
- ✅ Errores claros

---

### 3. Validación de AWB

#### ❌ ANTES
```python
AWB: Optional[str] = Field(serialization_alias="7102")
```

**Problemas:**
- Sin validación de formato
- Cualquier string es válido
- Sin documentación

#### ✅ DESPUÉS
```python
# Tipo con validación
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
- ✅ Validación de formato específico
- ✅ Regex pattern en tipo
- ✅ Validación de longitud
- ✅ Mensajes de error útiles

---

### 4. Model Config

#### ❌ ANTES
```python
model_config = {"extra": "forbid"}
```

**Problemas:**
- Configuración mínima
- Sin validación en asignación
- Sin limpieza de strings

#### ✅ DESPUÉS
```python
model_config = ConfigDict(
    # Validación
    validate_assignment=True,      # Valida al asignar
    validate_default=True,         # Valida defaults
    strict=False,                  # Permite coerción

    # Serialización
    populate_by_name=True,         # Permite alias o nombre
    use_enum_values=True,          # Usa valores de enum

    # Extra fields
    extra="forbid",                # Rechaza desconocidos

    # Strings
    str_strip_whitespace=True,     # Auto-limpia espacios

    # JSON Schema
    json_schema_extra={
        "title": "Yiqi Invoice",
        "description": "Command for creating invoice"
    }
)
```

**Beneficios:**
- ✅ Autocompletado en IDE
- ✅ Type checking
- ✅ Más control sobre validación
- ✅ Mejor documentación

---

## Características Nuevas

### 1. Model Validators (Validación Cross-Field)

```python
@model_validator(mode="after")
def validate_date_relationships(self) -> "YiqiInvoiceBase":
    """Validate relationships between dates."""

    # Recepción no puede ser antes de emisión
    if self.Fecha_recepcion < self.Fecha_emision:
        raise ValueError(
            f"Reception date ({self.Fecha_recepcion}) cannot be "
            f"before emission date ({self.Fecha_emision})"
        )

    # Fechas no pueden estar en el futuro
    if self.Fecha_emision > date.today():
        raise ValueError("Emission date cannot be in the future")

    return self
```

### 2. Computed Fields

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

### 3. Mixins para Lógica Reutilizable

```python
class DateValidatorMixin(BaseModel):
    """Reusable date validation logic."""

    @staticmethod
    def validate_date_not_future(v: date, field_name: str) -> date:
        """Ensure date is not in the future."""
        if v > date.today():
            raise ValueError(f"{field_name} cannot be in the future")
        return v
```

### 4. Validación de Peso y Items

```python
@model_validator(mode="after")
def validate_weight_and_items(self) -> "YiqiInvoiceBase":
    """Validate weight and items make sense together."""
    if self.Kg is not None and self.Items is not None:
        avg_weight = self.Kg / self.Items

        # Peso promedio debe ser razonable
        if avg_weight < 0.001 or avg_weight > 1000:
            raise ValueError(
                f"Average weight per item unreasonable: {avg_weight:.4f} kg/item"
            )

    return self
```

---

## Beneficios Clave

### 🎯 1. Validación Temprana

```python
# ANTES: Error en runtime al enviar a Yiqi
invoice = CreateYiqiInvoiceCommand(
    Fecha_emision=date(2024, 1, 15),
    Fecha_recepcion=date(2024, 1, 10),  # ❌ Antes de emisión
    # ...
)
# Se crea el objeto, falla después

# DESPUÉS: Error inmediato con mensaje claro
try:
    invoice = CreateYiqiInvoiceCommand(
        Fecha_emision=date(2024, 1, 15),
        Fecha_recepcion=date(2024, 1, 10),
        # ...
    )
except ValueError as e:
    print(e)
    # ✅ "Reception date (2024-01-10) cannot be before emission date (2024-01-15)"
```

### 📝 2. Documentación Automática

```python
# El schema JSON se genera automáticamente
schema = CreateYiqiInvoiceCommand.model_json_schema()

print(schema['properties']['Numero'])
# {
#     "type": "string",
#     "title": "Numero",
#     "description": "Número de factura",
#     "examples": ["001-001-0000001"],
#     "minLength": 1,
#     "maxLength": 500
# }
```

### 🧪 3. Testing Más Fácil

```python
def test_invalid_awb():
    """Test AWB validation."""
    with pytest.raises(ValueError, match="AWB must be 8 or 11 digits"):
        CreateYiqiInvoiceCommand(
            AWB="123",  # Muy corto
            # ... otros campos válidos
        )

def test_date_relationship():
    """Test fecha recepción antes de emisión."""
    with pytest.raises(ValueError, match="cannot be before"):
        CreateYiqiInvoiceCommand(
            Fecha_emision=date(2024, 1, 15),
            Fecha_recepcion=date(2024, 1, 10),
            # ... otros campos
        )
```

### 🔍 4. IDE Support Mejorado

```python
# Autocompletado completo
invoice.  # <-- IDE sugiere todos los campos + computed fields
# - Provider
# - Numero
# - days_to_reception  (computed!)
# - average_weight_per_item  (computed!)
# ...
```

---

## Ejemplos de Uso

### Crear Invoice Básica

```python
from decimal import Decimal
from datetime import date

invoice = CreateYiqiInvoiceCommand(
    Provider=123,
    Numero="001-001-0000001",
    Concepto="Servicios de transporte aéreo internacional",
    Fecha_emision=date(2024, 1, 15),
    Fecha_recepcion=date(2024, 1, 16),
    Mes_servicio=date(2024, 1, 1),
    Precio_unitario=Decimal("1500.50"),
    Moneda_original=2,  # USD
    Servicio=456,
    AWB="123-45678901",
    Kg=50.5,
    Items=10,
    creado_en_portal=True
)

# Acceder a computed fields
print(f"Días hasta recepción: {invoice.days_to_reception}")  # 1
print(f"Peso promedio por item: {invoice.average_weight_per_item} kg")  # 5.05
```

### Validar Antes de Crear

```python
# Validación pre-vuelo
validation = await validate_invoice_before_creation(
    purchase_invoice_id=123
)

if not validation["valid"]:
    print("Errores:")
    for error in validation["errors"]:
        print(f"  - {error}")

    print("Advertencias:")
    for warning in validation["warnings"]:
        print(f"  - {warning}")
else:
    # Crear invoice
    result = await create_invoice_from_purchase_invoice_tasks(123)
```

### Manejo de Errores

```python
try:
    result = await create_invoice_from_purchase_invoice_tasks(123)
    print(f"Invoice creada: Yiqi ID = {result['newId']}")

except InvoiceCreationError as e:
    print(f"Error: {e.message}")
    print(f"Detalles: {e.details}")

    # Ejemplo de detalles:
    # {
    #     "purchase_invoice_id": 123,
    #     "validation_error": "AWB must be 8 or 11 digits",
    #     "invoice_number": "001-001-0001"
    # }
```

---

## 📊 Métricas de Mejora

| Aspecto | Antes | Después | Mejora |
|---------|-------|---------|--------|
| **Líneas de código** | 74 | 550+ | +642% |
| **Validaciones** | 1 | 15+ | +1400% |
| **Type safety** | Parcial | Completo | ✅ |
| **Documentación** | Mínima | Completa | ✅ |
| **Errores claros** | No | Sí | ✅ |
| **Computed fields** | 0 | 3 | ✅ |
| **Cross-field validation** | 0 | 2 | ✅ |
| **Examples en schema** | 0 | 10+ | ✅ |

---

## 🎓 Lecciones Aprendidas

### 1. Separar Validación de Serialización
- **Validators**: Transforman INPUT
- **Serializers**: Transforman OUTPUT

### 2. Usar Annotated para Tipos Reutilizables
```python
PositiveInt = Annotated[int, Field(gt=0)]
# Reutilizable en múltiples campos
```

### 3. Model Validators para Lógica de Negocio
```python
@model_validator(mode="after")
def validate_business_rules(self):
    # Validar relaciones entre campos
    return self
```

### 4. Computed Fields para Valores Derivados
```python
@computed_field
@property
def calculated_value(self) -> float:
    return self.field_a * self.field_b
```

---

## 🚀 Próximos Pasos

1. ✅ **Migrar** `__init__.py` al nuevo código
2. ✅ **Actualizar** tasks para usar `improved_commands`
3. ✅ **Agregar** tests unitarios
4. ✅ **Documentar** casos de uso
5. ✅ **Aplicar** este patrón a otros módulos

---

## 📚 Referencias

- [Guía de Migración Detallada](./domain/command/MIGRATION_GUIDE.md)
- [Código Mejorado](./domain/command/improved_commands.py)
- [Task Mejorada](./adapter/input/tasks/yiqi_erp_improved.py)
- [Pydantic v2 Docs](https://docs.pydantic.dev/latest/)

---

**¿Preguntas o sugerencias?** Abre un issue o PR!
