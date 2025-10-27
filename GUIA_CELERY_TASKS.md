# Guía de Celery Tasks Simplificado

## Arquitectura Refactorizada

Este proyecto ahora usa un sistema **simplificado** de Celery tasks basado en el `service_locator`, eliminando la complejidad del sistema anterior de múltiples instancias de Celery.

---

## Cambios Principales

### ANTES (Sistema Complejo)

```python
# Cada módulo tenía su propia instancia de Celery
from celery import Celery
from core.config.settings import env

app = Celery("invoicing", broker=env.RABBITMQ_URL, backend=env.REDIS_URL)

@app.task
def emit_invoice():
    return "Done"
```

**Problemas:**
- Múltiples instancias de Celery
- Discovery complejo que buscaba instancias
- Merge manual de tasks
- Configuración duplicada

### AHORA (Sistema Simplificado)

```python
# Tasks son funciones Python normales
def emit_invoice():
    """Task para emitir factura"""
    return "Done"
```

**Ventajas:**
- Una sola instancia de Celery
- Tasks son funciones normales
- Discovery automático desde service_locator
- Configuración centralizada
- Fácil testing

---

## Cómo Funciona

### 1. Definir Tasks (Input Adapter)

Las tasks se definen como **funciones Python normales** en cada módulo:

**Ubicación:** `modules/{module}/adapter/input/tasks/`

```python
# modules/invoicing/adapter/input/tasks/invoice.py
"""
Tasks del módulo Invoicing - Input Adapter.
"""

def emit_invoice():
    """
    Task para emitir factura.

    Será registrada automáticamente como: "invoicing.emit_invoice"
    """
    import time
    time.sleep(10)
    return "Factura emitida!"

def process_refund(invoice_id: int):
    """Task para procesar reembolso"""
    return f"Reembolso procesado para invoice {invoice_id}"
```

### 2. Registrar Tasks en module.py

Las tasks se registran en el `service_locator` a través del `module.py`:

```python
# modules/invoicing/module.py
from shared.interfaces.module_registry import ModuleInterface
from typing import Dict

class InvoicingModule(ModuleInterface):

    @property
    def service(self) -> Dict[str, object]:
        # Importar las tasks como funciones normales
        from .adapter.input.tasks import invoice

        return {
            "purchase_invoice_service": self._container.purchase_invoice_service,
            # Exponer las tasks como un dict de callables
            "invoicing_tasks": {
                "emit_invoice": invoice.emit_invoice,
            },
        }
```

**Convención de nombres:**
- El servicio debe terminar en `_tasks`
- Formato: `{module_name}_tasks`
- Ejemplos: `invoicing_tasks`, `yiqi_erp_tasks`, `notifications_tasks`

### 3. Discovery Automático

El sistema descubre automáticamente todas las tasks desde el `service_locator`:

```python
# core/celery/discovery.py
from celery import Celery
from core.config.settings import env

def create_celery_worker() -> Celery:
    """Crea el worker de Celery con todas las tasks descubiertas"""
    from shared.interfaces.service_locator import service_locator

    # Crear una única instancia de Celery
    app = Celery("hexa_worker", broker=env.RABBITMQ_URL, backend=env.REDIS_URL)

    # Obtener todos los servicios que terminan en "_tasks"
    task_services = {
        name: service
        for name, service in service_locator._services.items()
        if name.endswith("_tasks")
    }

    # Registrar cada función como task de Celery
    for service_name, task_dict in task_services.items():
        module_name = service_name.replace("_tasks", "")

        for task_name, task_func in task_dict.items():
            # Registrar con nombre: "invoicing.emit_invoice"
            full_task_name = f"{module_name}.{task_name}"
            app.task(name=full_task_name)(task_func)
            print(f"  ✓ Registered: {full_task_name}")

    return app
```

### 4. Iniciar el Worker

```bash
# Comando simplificado
uv run hexa celery-apps
```

```python
# hexa/__main__.py
@cmd.command("celery-apps")
def run_celery():
    """Inicia el worker de Celery con todas las tasks descubiertas"""
    from core.celery.discovery import create_celery_worker

    app = create_celery_worker()
    app.worker_main(["worker", "--loglevel=INFO"])
```

**Output esperado:**
```
📦 Discovered 3 task services from service_locator
  ✓ Registered: invoicing.emit_invoice
  ✓ Registered: yiqi_erp.emit_invoice
  ✓ Registered: notifications.send_notification

✅ Total 3 tasks registered in Celery worker
```

---

## Uso de Tasks

### Desde Endpoints (API)

```python
# modules/invoicing/adapter/input/api/v1/purchase_invoice.py
from shared.interfaces.service_locator import service_locator

@purchase_invoice_router.post("")
async def create_purchase_invoice(
    purchase_invoice: CreatePurchaseInvoiceRequest,
    emit_to_yiqi: bool,
):
    invoice = await service.create(purchase_invoice)
    invoice_saved = await service.save(invoice)

    # Ejecutar task de Celery de forma asíncrona
    if emit_to_yiqi:
        yiqi_tasks = service_locator.get_service("yiqi_erp_tasks")
        yiqi_tasks["emit_invoice"].delay(invoice_saved.model_dump())

    return invoice_saved
```

### Desde Otros Módulos

```python
# modules/accounting/application/service/accounting.py
from shared.interfaces.service_locator import service_locator

class AccountingService:

    async def process_invoice(self, invoice_id: int):
        # Obtener tasks de invoicing
        invoicing_tasks = service_locator.get_service("invoicing_tasks")

        # Ejecutar task de forma asíncrona
        invoicing_tasks["emit_invoice"].delay()

        # O con apply_async para más opciones
        invoicing_tasks["emit_invoice"].apply_async(
            countdown=60,  # Ejecutar en 60 segundos
            retry=True,
        )
```

### Testing de Tasks

```python
# tests/test_invoicing_tasks.py
from modules.invoicing.adapter.input.tasks.invoice import emit_invoice

def test_emit_invoice():
    # Las tasks son funciones normales, fáciles de testear
    result = emit_invoice()
    assert result == "Factura emitida!"
```

---

## Type Safety con Protocols

Para tener **autocompletado** y **type checking**, se crearon protocols en `shared/interfaces/service_protocols.py`:

```python
# shared/interfaces/service_protocols.py

class InvoicingTasksProtocol(Protocol):
    """API pública de tasks de Celery del módulo Invoicing"""

    def emit_invoice(self) -> str:
        """
        Task para emitir factura.

        Usage:
            tasks = service_locator.get_service("invoicing_tasks")
            tasks["emit_invoice"].delay()
        """
        ...

class YiqiERPTasksProtocol(Protocol):
    """API pública de tasks de Celery del módulo YiqiERP"""

    def emit_invoice(self, data: Any) -> str:
        """Task para emitir factura al ERP externo"""
        ...
```

**Uso con type hints:**

```python
from shared.interfaces.service_protocols import InvoicingTasksProtocol
from shared.interfaces.service_locator import service_locator

# Con type hint
tasks: InvoicingTasksProtocol = service_locator.get_service("invoicing_tasks")
tasks["emit_invoice"].delay()  # Autocompletado funciona!
```

---

## Agregar Nueva Task

### Paso 1: Crear la función

```python
# modules/accounting/adapter/input/tasks/accounting.py
"""Tasks del módulo Accounting"""

def generate_report(start_date: str, end_date: str):
    """
    Task para generar reporte contable.

    Será registrada como: "accounting.generate_report"
    """
    # Lógica del reporte
    return f"Reporte generado: {start_date} - {end_date}"
```

### Paso 2: Registrar en module.py

```python
# modules/accounting/module.py

@property
def service(self) -> Dict[str, object]:
    from .adapter.input.tasks import accounting

    return {
        "accounting_service": self._container.accounting_service,
        "accounting_tasks": {
            "generate_report": accounting.generate_report,
        },
    }
```

### Paso 3: (Opcional) Crear Protocol

```python
# shared/interfaces/service_protocols.py

class AccountingTasksProtocol(Protocol):
    """API pública de tasks del módulo Accounting"""

    def generate_report(self, start_date: str, end_date: str) -> str:
        """Task para generar reporte contable"""
        ...
```

### Paso 4: Reiniciar el worker

```bash
# El worker detectará automáticamente la nueva task
uv run hexa celery-apps
```

**Output:**
```
📦 Discovered 4 task services from service_locator
  ✓ Registered: invoicing.emit_invoice
  ✓ Registered: yiqi_erp.emit_invoice
  ✓ Registered: notifications.send_notification
  ✓ Registered: accounting.generate_report

✅ Total 4 tasks registered in Celery worker
```

### Paso 5: Usar la task

```python
from shared.interfaces.service_locator import service_locator

tasks = service_locator.get_service("accounting_tasks")
tasks["generate_report"].delay("2025-01-01", "2025-01-31")
```

---

## Comparación con Sistema Anterior

| Aspecto | Antes (Complejo) | Ahora (Simplificado) |
|---------|------------------|----------------------|
| **Instancias Celery** | Una por módulo | Una global |
| **Definición de tasks** | `@app.task` decorator | Funciones normales |
| **Discovery** | Escanea archivos buscando instancias | Lee desde service_locator |
| **Registro** | Merge manual de instancias | Automático con `app.task()` |
| **Testing** | Difícil (decoradores) | Fácil (funciones puras) |
| **Type safety** | No | Sí (con Protocols) |
| **Configuración** | Duplicada en cada módulo | Centralizada |
| **Líneas de código** | ~100 líneas | ~30 líneas |

---

## Ventajas del Nuevo Sistema

1. **Simplicidad:** Tasks son funciones Python normales
2. **Consistencia:** Usa el mismo patrón que otros servicios (service_locator)
3. **Type Safety:** Protocols permiten autocompletado y type checking
4. **Testing:** Funciones puras sin decoradores mágicos
5. **Mantenimiento:** Menos código, más fácil de entender
6. **Escalabilidad:** Agregar nuevas tasks es trivial
7. **Arquitectura Hexagonal:** Tasks como input adapters, consistente con el diseño

---

## Troubleshooting

### Task no se registra

**Problema:** La task no aparece en el worker

**Solución:**
1. Verifica que el servicio termine en `_tasks`
2. Verifica que esté en `module.py` dentro de `service`
3. Reinicia el worker: `uv run hexa celery-apps`

### Task no se ejecuta

**Problema:** `.delay()` no hace nada

**Solución:**
1. Verifica que el worker esté corriendo
2. Verifica que RabbitMQ esté corriendo: `docker ps`
3. Revisa logs del worker para errores

### Type hints no funcionan

**Problema:** No hay autocompletado

**Solución:**
1. Verifica que el Protocol exista en `service_protocols.py`
2. Usa type hints: `tasks: InvoicingTasksProtocol = service_locator.get_service(...)`
3. Reinicia el LSP de tu editor

---

## Archivos Modificados

- **[core/celery/discovery.py](backend/core/celery/discovery.py)** - Sistema de discovery simplificado
- **[hexa/__main__.py](backend/hexa/__main__.py)** - Comando para iniciar worker
- **[shared/interfaces/service_protocols.py](backend/shared/interfaces/service_protocols.py)** - Protocols para type safety
- **[modules/invoicing/module.py](backend/modules/invoicing/module.py)** - Registro de tasks
- **[modules/invoicing/adapter/input/tasks/invoice.py](backend/modules/invoicing/adapter/input/tasks/invoice.py)** - Task como función normal
- **[modules/yiqi_erp/adapter/input/tasks/yiqi_erp.py](backend/modules/yiqi_erp/adapter/input/tasks/yiqi_erp.py)** - Task refactorizada
- **[modules/notifications/module.py](backend/modules/notifications/module.py)** - Nuevo módulo
- **[modules/notifications/adapter/input/tasks/notification.py](backend/modules/notifications/adapter/input/tasks/notification.py)** - Task refactorizada

---

**Fecha:** 2025-10-23
**Sistema:** Celery Tasks Simplificado con service_locator