# Módulos de Negocio

Los módulos de negocio implementan funcionalidades específicas del dominio empresarial y pueden operar de forma independiente.

## 💰 Finance Module

**Ubicación**: `modules/finance/`
**Propósito**: Gestión financiera y contable

### Funcionalidades
- Gestión de monedas
- Cálculos financieros
- Entradas contables
- Órdenes de pago
- Retenciones fiscales

### Componentes Principales

#### Domain
```python
# domain/entity/currency.py
class Currency:
    def __init__(self, code: str, name: str, symbol: str):
        self.code = code.upper()
        self.name = name
        self.symbol = symbol
        self.is_active = True
        self.exchange_rate = Decimal('1.0')

# domain/entity/accounting_entry.py
class AccountingEntry:
    def __init__(self, account: str, debit: Money, credit: Money):
        self.account = account
        self.debit = debit
        self.credit = credit
        self.date = datetime.now()
        self._validate_balance()

# domain/vo/money.py
@dataclass
class Money:
    amount: Decimal
    currency: Currency
    
    def add(self, other: 'Money') -> 'Money':
        if self.currency != other.currency:
            raise CurrencyMismatchError()
        return Money(self.amount + other.amount, self.currency)
```

#### Application
```python
# application/service/currency.py
class CurrencyService:
    def create_currency(self, code: str, name: str, symbol: str) -> CurrencyDTO:
        currency = Currency(code, name, symbol)
        saved = self.repository.save(currency)
        return CurrencyDTO.from_entity(saved)
    
    def convert_currency(self, amount: Money, target_currency: Currency) -> Money:
        if amount.currency == target_currency:
            return amount
        
        rate = self._get_exchange_rate(amount.currency, target_currency)
        converted_amount = amount.amount * rate
        return Money(converted_amount, target_currency)
```

#### Endpoints
- `GET /finance/currencies` - Listar monedas
- `POST /finance/currencies` - Crear moneda
- `POST /finance/convert` - Convertir moneda
- `GET /finance/accounting-entries` - Entradas contables

---

## 🏢 Provider Module

**Ubicación**: `modules/provider/`
**Propósito**: Gestión de proveedores y facturas de compra

### Funcionalidades
- CRUD de proveedores
- Facturas de compra borrador
- Integración con sistemas externos
- Gestión de documentos

### Componentes Principales

#### Domain
```python
# domain/entity/provider.py
class Provider:
    def __init__(self, name: str, tax_id: str, email: str):
        self.name = name
        self.tax_id = self._validate_tax_id(tax_id)
        self.email = self._validate_email(email)
        self.is_active = True
        self.created_at = datetime.now()
    
    def deactivate(self) -> None:
        self.is_active = False

# domain/entity/draft_purchase_invoice.py
class DraftPurchaseInvoice:
    def __init__(self, provider_id: int, total_amount: Money):
        self.provider_id = provider_id
        self.total_amount = total_amount
        self.status = InvoiceStatus.DRAFT
        self.items: List[InvoiceItem] = []
        self.created_at = datetime.now()
    
    def add_item(self, description: str, quantity: int, unit_price: Money) -> None:
        item = InvoiceItem(description, quantity, unit_price)
        self.items.append(item)
        self._recalculate_total()
```

#### Application
```python
# application/service/provider.py
class ProviderService:
    def create_provider(self, name: str, tax_id: str, email: str) -> ProviderDTO:
        provider = Provider(name, tax_id, email)
        saved = self.repository.save(provider)
        
        # Publicar evento
        event = DomainEvent(
            event_type="provider_created",
            data={"provider_id": saved.id, "name": name},
            timestamp=datetime.now(),
            module_source="provider"
        )
        event_bus.publish(event)
        
        return ProviderDTO.from_entity(saved)

# application/service/draft_purchase_invoice.py
class DraftPurchaseInvoiceService:
    def create_draft_invoice(self, provider_id: int, 
                           total_amount: Money) -> DraftInvoiceDTO:
        draft = DraftPurchaseInvoice(provider_id, total_amount)
        saved = self.repository.save(draft)
        return DraftInvoiceDTO.from_entity(saved)
```

#### Endpoints
- `GET /providers` - Listar proveedores
- `POST /providers` - Crear proveedor
- `GET /providers/{id}` - Obtener proveedor
- `POST /providers/{id}/invoices/draft` - Crear factura borrador

---

## 🔌 YiQi ERP Module

**Ubicación**: `modules/yiqi_erp/`
**Propósito**: Integración con sistema ERP externo YiQi

### Funcionalidades
- Sincronización de datos
- Creación de facturas
- Gestión de empresas
- Órdenes de pago
- Notas de crédito

### Componentes Principales

#### Domain
```python
# domain/entity/factura.py
class Factura:
    def __init__(self, numero: str, empresa_id: int, total: Money):
        self.numero = numero
        self.empresa_id = empresa_id
        self.total = total
        self.fecha = datetime.now()
        self.estado = EstadoFactura.PENDIENTE

# domain/entity/empresa.py
class Empresa:
    def __init__(self, nombre: str, ruc: str):
        self.nombre = nombre
        self.ruc = self._validate_ruc(ruc)
        self.activa = True

# domain/entity/orden_pago.py
class OrdenPago:
    def __init__(self, factura_id: int, monto: Money, fecha_pago: date):
        self.factura_id = factura_id
        self.monto = monto
        self.fecha_pago = fecha_pago
        self.estado = EstadoPago.PENDIENTE
```

#### Application
```python
# application/service/yiqi.py
class YiqiService:
    def __init__(self, yiqi_repository: YiqiRepository):
        self.repository = yiqi_repository
    
    def create_invoice_in_yiqi(self, invoice_data: dict) -> YiqiInvoiceDTO:
        # Transformar datos al formato YiQi
        yiqi_format = self._transform_to_yiqi_format(invoice_data)
        
        # Enviar a YiQi
        response = self.repository.create_invoice(yiqi_format)
        
        # Transformar respuesta
        return YiqiInvoiceDTO.from_yiqi_response(response)
    
    def sync_companies(self) -> List[EmpresaDTO]:
        companies = self.repository.get_companies()
        return [EmpresaDTO.from_yiqi_data(c) for c in companies]
```

#### Output Adapters
```python
# adapter/output/api/yiqi_rest.py
class YiqiApiRepository(YiqiRepository):
    def __init__(self, client: YiqiHttpClient):
        self.client = client
    
    def create_invoice(self, invoice_data: dict) -> dict:
        response = self.client.post("/facturas", json=invoice_data)
        return response.json()
    
    def get_companies(self) -> List[dict]:
        response = self.client.get("/empresas")
        return response.json()["data"]
```

#### Endpoints
- `POST /yiqi/sync/companies` - Sincronizar empresas
- `POST /yiqi/invoices` - Crear factura en YiQi
- `GET /yiqi/invoices/{id}` - Obtener factura de YiQi
- `POST /yiqi/payment-orders` - Crear orden de pago

---

## 📄 Invoicing Module

**Ubicación**: `modules/invoicing/`
**Propósito**: Gestión de facturación interna

### Funcionalidades
- Facturas de venta
- Notas de crédito
- Series de facturación
- Cancelaciones
- Numeración automática

### Componentes Principales

#### Domain
```python
# domain/entity/invoice.py
class Invoice:
    def __init__(self, series: Series, customer_id: int):
        self.series = series
        self.customer_id = customer_id
        self.number = self._generate_number()
        self.items: List[InvoiceItem] = []
        self.status = InvoiceStatus.DRAFT
        self.created_at = datetime.now()
    
    def add_item(self, description: str, quantity: int, unit_price: Money) -> None:
        item = InvoiceItem(description, quantity, unit_price)
        self.items.append(item)
        self._recalculate_totals()
    
    def finalize(self) -> None:
        if not self.items:
            raise EmptyInvoiceError()
        self.status = InvoiceStatus.FINALIZED
        self.finalized_at = datetime.now()

# domain/vo/invoice_number.py
@dataclass
class InvoiceNumber:
    series: str
    sequential: int
    
    def __str__(self) -> str:
        return f"{self.series}-{self.sequential:08d}"
```

#### Endpoints
- `GET /invoicing/invoices` - Listar facturas
- `POST /invoicing/invoices` - Crear factura
- `POST /invoicing/invoices/{id}/finalize` - Finalizar factura
- `POST /invoicing/credit-notes` - Crear nota de crédito

---

## 🛒 Procurement Module

**Ubicación**: `modules/procurement/`
**Propósito**: Gestión de compras y adquisiciones

### Funcionalidades
- Órdenes de compra
- Facturas de compra
- Seguimiento de pedidos
- Aprobaciones

### Componentes Principales

#### Domain
```python
# domain/entity/purchase_order.py
class PurchaseOrder:
    def __init__(self, provider_id: int, requested_by: int):
        self.provider_id = provider_id
        self.requested_by = requested_by
        self.status = PurchaseOrderStatus.DRAFT
        self.items: List[PurchaseOrderItem] = []
        self.created_at = datetime.now()
    
    def submit_for_approval(self) -> None:
        if not self.items:
            raise EmptyOrderError()
        self.status = PurchaseOrderStatus.PENDING_APPROVAL
        self.submitted_at = datetime.now()

# domain/entity/purchase_invoice.py
class PurchaseInvoice:
    def __init__(self, purchase_order_id: int, invoice_number: str):
        self.purchase_order_id = purchase_order_id
        self.invoice_number = invoice_number
        self.status = PurchaseInvoiceStatus.RECEIVED
        self.received_at = datetime.now()
```

#### Endpoints
- `GET /procurement/purchase-orders` - Listar órdenes
- `POST /procurement/purchase-orders` - Crear orden
- `POST /procurement/purchase-orders/{id}/approve` - Aprobar orden
- `POST /procurement/purchase-invoices` - Registrar factura

## Comunicación Entre Módulos de Negocio

### Ejemplo: Provider → Finance
```python
# Cuando se crea un proveedor, Finance puede necesitar configurar cuentas
class FinanceProviderHandler(EventHandler):
    def handle(self, event: DomainEvent) -> None:
        if event.event_type == "provider_created":
            provider_id = event.data["provider_id"]
            # Crear cuenta contable para el proveedor
            self.create_provider_account(provider_id)
```

### Ejemplo: YiQi ERP → Invoicing
```python
# Sincronización de facturas entre sistemas
class InvoicingSyncHandler(EventHandler):
    def handle(self, event: DomainEvent) -> None:
        if event.event_type == "yiqi_invoice_created":
            yiqi_invoice = event.data["invoice"]
            # Crear factura local basada en YiQi
            self.create_local_invoice(yiqi_invoice)
```

## Configuración de Módulos de Negocio

### Variables de Entorno
```bash
# YiQi ERP
YIQI_BASE_URL=https://api.yiqi.com
YIQI_API_TOKEN=your_token_here
YIQI_TIMEOUT=30

# Finance
DEFAULT_CURRENCY=USD
EXCHANGE_RATE_PROVIDER=fixer.io
ACCOUNTING_PRECISION=2

# Provider
MAX_PROVIDERS_PER_PAGE=50
PROVIDER_DOCUMENT_STORAGE=s3
```

### Health Checks Específicos
```python
@router.get("/health")
async def yiqi_health():
    try:
        response = await yiqi_client.ping()
        return {
            "module": "yiqi_erp",
            "status": "healthy",
            "yiqi_connection": "ok",
            "last_sync": get_last_sync_time()
        }
    except Exception as e:
        return {
            "module": "yiqi_erp",
            "status": "unhealthy",
            "error": str(e)
        }
```