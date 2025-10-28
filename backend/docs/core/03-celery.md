# Celery - Sistema de Tareas Asíncronas

## Arquitectura

El proyecto usa **un solo worker de Celery** que descubre automáticamente todas las tasks de todos los módulos mediante el `service_locator`.

## Cómo Funciona

### 1. Registro de Tasks en Módulos

Las tasks se definen como funciones Python normales (sin decorador `@app.task`):

```python
# modules/invoicing/adapter/input/tasks/invoice.py
import time

def emit_invoice():
    """Task para emitir factura"""
    time.sleep(10)
    return "Factura emitida!"
```

### 2. Registro en module.py

```python
# modules/invoicing/module.py
@property
def service(self) -> Dict[str, object]:
    from .adapter.input.tasks import invoice
    
    return {
        "purchase_invoice_service": self._container.purchase_invoice_service,
        # Registrar tasks
        "invoicing_tasks": {
            "emit_invoice": invoice.emit_invoice,
        },
    }
```

**Importante**: El nombre debe terminar en `_tasks` para que sea descubierto.

### 3. Descubrimiento Automático

```python
# core/celery/discovery.py
def create_celery_worker() -> Celery:
    app = Celery("hexa_worker", broker=env.RABBITMQ_URL, backend=env.REDIS_URL)
    
    # Buscar todos los servicios que terminan en "_tasks"
    task_services = {
        name: service
        for name, service in service_locator._services.items()
        if name.endswith("_tasks")
    }
    
    # Registrar cada función como task
    for service_name, task_dict in task_services.items():
        module_name = service_name.replace("_tasks", "")
        for task_name, task_func in task_dict.items():
            full_task_name = f"{module_name}.{task_name}"
            app.task(name=full_task_name)(task_func)
    
    return app
```

### 4. Ejecución del Worker

```python
# hexa/__main__.py
@cmd.command("celery-apps")
def run_celery():
    # Limpiar registros (para hot-reload)
    ModuleRegistry().clear()
    service_locator.clear()
    
    # Descubrir módulos
    discover_modules("modules", "module.py")
    
    # Crear worker con tasks
    app = create_celery_worker()
    app.worker_main(["worker", "--loglevel=INFO"])
```

## Usar Tasks

### Desde Python

```python
from celery import Celery

app = Celery("hexa_worker", broker=env.RABBITMQ_URL)

# Ejecutar task asíncronamente
result = app.send_task("invoicing.emit_invoice")

# Esperar resultado
result.get(timeout=30)
```

### Desde un Endpoint

```python
@router.post("/emit")
async def emit_invoice():
    from celery import Celery
    app = Celery("hexa_worker", broker=env.RABBITMQ_URL)
    
    result = app.send_task("invoicing.emit_invoice")
    
    return {"task_id": result.id, "status": "pending"}
```

### Desde el Shell

```bash
# Dentro del container
docker compose -f compose.dev.yaml exec backend python

>>> from celery import Celery
>>> app = Celery("hexa_worker", broker="amqp://hexa:hexa@rabbit:5672/")
>>> result = app.send_task("invoicing.emit_invoice")
>>> result.get()
'Factura emitida!'
```

## Monitorear Tasks

### Ver logs del worker

```bash
docker compose -f compose.dev.yaml logs -f celery_worker
```

### Ver tasks registradas

Al iniciar el worker, verás:

```
📦 Discovered 3 task services from service_locator
  ✓ Registered: invoicing.emit_invoice
  ✓ Registered: notifications.send_notification
  ✓ Registered: yiqi_erp.emit_invoice

✅ Total 3 tasks registered in Celery worker
```

### RabbitMQ Management

http://localhost:15672
- User: hexa
- Pass: hexa

Puedes ver:
- Queues activas
- Tasks pendientes
- Mensajes procesados

## Tasks con Parámetros

```python
# modules/notifications/adapter/input/tasks/notification.py
def send_notification(user_id: int, message: str):
    """Enviar notificación a usuario"""
    print(f"Sending to user {user_id}: {message}")
    return "Sent"

# Registrar
"notifications_tasks": {
    "send_notification": notification.send_notification,
}

# Usar
app.send_task("notifications.send_notification", args=[123, "Hello!"])
```

## Tasks Asíncronas (async/await)

El sistema **soporta automáticamente funciones `async`**. Las envuelve en un wrapper síncrono usando `asyncio.run()`:

```python
# modules/yiqi_erp/adapter/input/tasks/yiqi_erp.py
async def create_invoice_from_purchase_invoice_tasks(
    purchase_invoice_id: int, company_id: int = 316
):
    """Task async - soportada automáticamente"""
    yiqi_service = YiqiContainer.service()
    purchase_invoice_service = service_locator.get_service("purchase_invoice_service")()

    # Usar await normalmente
    purchase_invoice = await purchase_invoice_service.get_one_by_id(purchase_invoice_id)
    yiqi_response = await yiqi_service.create_invoice(...)

    return yiqi_response

# Registrar igual que una función síncrona
"yiqi_erp_tasks": {
    "create_invoice_from_purchase_invoice_tasks": {
        "task": create_invoice_from_purchase_invoice_tasks,
        "config": {...}
    }
}
```

**Al registrarse, verás**:
```
✓ Registered: yiqi_erp.create_invoice_from_purchase_invoice_tasks [async] (autoretry_for=...)
```

El marcador `[async]` indica que la función fue envuelta automáticamente.

### Ventajas de Tasks Async

- ✅ Código limpio y consistente con el resto del proyecto
- ✅ Usa `await` con servicios async (repositorios, APIs, etc.)
- ✅ No necesitas `asyncio.run()` manual
- ✅ Compatible con reintentos automáticos de Celery

## Tasks con Retry y Configuración Avanzada

El sistema ahora soporta dos formatos para registrar tasks:

### Formato Simple (sin configuración)

```python
# modules/invoicing/module.py
@property
def service(self) -> Dict[str, object]:
    from .adapter.input.tasks import invoice

    return {
        "invoicing_tasks": {
            "emit_invoice": invoice.emit_invoice,  # Función directa
        },
    }
```

### Formato Avanzado (con configuración de reintentos)

```python
# modules/yiqi_erp/module.py
@property
def service(self) -> Dict[str, object]:
    from .adapter.input.tasks.yiqi_erp import (
        create_invoice_from_purchase_invoice_tasks,
    )

    return {
        "yiqi_erp_tasks": {
            "create_invoice_from_purchase_invoice_tasks": {
                "task": create_invoice_from_purchase_invoice_tasks,
                "config": {
                    "autoretry_for": (Exception,),  # Reintentar en cualquier excepción
                    "retry_kwargs": {"max_retries": 5},  # Máximo 5 reintentos
                    "retry_backoff": True,  # Backoff exponencial
                    "retry_backoff_max": 600,  # Máximo 10 minutos de espera
                    "retry_jitter": True,  # Añadir jitter aleatorio
                },
            }
        },
    }
```

### Opciones de Configuración Disponibles

| Parámetro | Descripción | Ejemplo |
|-----------|-------------|---------|
| `autoretry_for` | Tupla de excepciones que disparan reintento automático | `(Exception,)`, `(ConnectionError, TimeoutError)` |
| `retry_kwargs` | Configuración de reintentos (`max_retries`) | `{"max_retries": 5}` |
| `retry_backoff` | Activar backoff exponencial entre reintentos | `True` |
| `retry_backoff_max` | Tiempo máximo de espera entre reintentos (segundos) | `600` (10 minutos) |
| `retry_jitter` | Añadir variación aleatoria al backoff | `True` |
| `bind` | Pasar la instancia de task como primer argumento | `True` |
| `max_retries` | Máximo de reintentos (alternativa a `retry_kwargs`) | `3` |
| `default_retry_delay` | Delay fijo entre reintentos (segundos) | `60` |

### Estrategias de Retry

#### 1. Retry con Backoff Exponencial (Recomendado)

```python
"config": {
    "autoretry_for": (Exception,),
    "retry_kwargs": {"max_retries": 5},
    "retry_backoff": True,  # 1s, 2s, 4s, 8s, 16s...
    "retry_backoff_max": 600,
    "retry_jitter": True,  # Previene thundering herd
}
```

**Cuándo usar**: APIs externas, servicios que pueden saturarse

#### 2. Retry con Delay Fijo

```python
"config": {
    "autoretry_for": (ConnectionError, TimeoutError),
    "max_retries": 3,
    "default_retry_delay": 60,  # 60s entre cada reintento
}
```

**Cuándo usar**: Servicios con rate limiting conocido

#### 3. Retry Solo para Errores Específicos

```python
"config": {
    "autoretry_for": (HTTPException,),  # Solo reintentar HTTPException
    "retry_kwargs": {"max_retries": 3},
}
```

**Cuándo usar**: Cuando quieres que ciertos errores fallen inmediatamente

### Comportamiento del Retry

Con la configuración anterior, cuando una task falla:

1. **Primera ejecución**: Falla con `Exception`
2. **Primer reintento**: Espera ~1s (con jitter)
3. **Segundo reintento**: Espera ~2s (con jitter)
4. **Tercer reintento**: Espera ~4s (con jitter)
5. **Cuarto reintento**: Espera ~8s (con jitter)
6. **Quinto reintento**: Espera ~16s (con jitter)
7. **Si falla**: La task se marca como FAILED definitivamente

### Cómo Llamar Tasks (send_task)

**IMPORTANTE**: Los parámetros de retry se configuran al REGISTRAR la task, NO al llamarla.

```python
# ✅ CORRECTO - Solo parámetros válidos de send_task
self.tasks_service.send_task(
    "yiqi_erp.create_invoice_from_purchase_invoice_tasks",
    args=[purchase_invoice.id],
    countdown=30,  # Delay antes de ejecutar (segundos)
    # Los reintentos YA están configurados en el módulo
)

# ❌ INCORRECTO - Estos parámetros NO existen en send_task
self.tasks_service.send_task(
    "yiqi_erp.create_invoice_from_purchase_invoice_tasks",
    args=[purchase_invoice.id],
    retries=3,  # ❌ NO existe
    retry_policy={...},  # ❌ NO existe
)
```

### Parámetros Válidos para send_task

- `args`: Argumentos posicionales para la task
- `kwargs`: Argumentos nombrados para la task
- `countdown`: Delay en segundos antes de ejecutar
- `eta`: Timestamp absoluto para ejecutar la task
- `expires`: Tiempo de expiración de la task
- `priority`: Prioridad de la task (0-9)
- `queue`: Cola específica para la task

### Monitorear Reintentos

En los logs del worker verás:

```
[2025-01-15 10:30:00] Task yiqi_erp.create_invoice_from_purchase_invoice_tasks[abc-123] received
[2025-01-15 10:30:01] Task yiqi_erp.create_invoice_from_purchase_invoice_tasks[abc-123] retry: Retry in 1s: Exception('Connection failed')
[2025-01-15 10:30:03] Task yiqi_erp.create_invoice_from_purchase_invoice_tasks[abc-123] retry: Retry in 2s: Exception('Connection failed')
[2025-01-15 10:30:06] Task yiqi_erp.create_invoice_from_purchase_invoice_tasks[abc-123] succeeded in 0.5s
```

## Tasks Periódicas (Cron)

Para tasks periódicas, usar Celery Beat (no implementado aún):

```python
# celery_beat_config.py
from celery.schedules import crontab

beat_schedule = {
    'sync-invoices-every-hour': {
        'task': 'invoicing.sync_invoices',
        'schedule': crontab(minute=0, hour='*/1'),
    },
}
```

## Hot Reload

El worker usa `watchfiles` para auto-reload:

```yaml
# compose.dev.yaml
celery_worker:
  command: /bin/sh -c "uv run watchfiles --filter python 'uv run hexa celery-apps' modules core shared"
```

Cuando cambias un archivo en `modules/`, `core/` o `shared/`, el worker se reinicia automáticamente.

## Buenas Prácticas

### ✅ DO

- Funciones puras sin efectos secundarios inesperados
- Idempotentes (pueden ejecutarse múltiples veces sin problemas)
- Con timeout razonable
- Logging claro

### ❌ DON'T

- Tasks que modifican estado global
- Tasks que dependen de otras tasks síncronamente
- Tasks sin manejo de errores
- Tasks con lógica de negocio compleja (usa use cases)

## Arquitectura Recomendada

```python
# ❌ MAL - Lógica en la task
def process_order():
    order = get_order()
    validate(order)
    calculate_total(order)
    save(order)

# ✅ BIEN - Task delgada, use case hace el trabajo
def process_order(order_id: int):
    from modules.orders.application.service.order import OrderService
    from shared.interfaces.service_locator import service_locator
    
    service = service_locator.get_service("order_service")
    return await service.process_order(order_id)
```

## Troubleshooting

### Tasks no aparecen

1. Verificar que el servicio termine en `_tasks`
2. Ver logs del worker: `docker compose logs celery_worker`
3. Verificar que el módulo está registrado

### Worker no se conecta a RabbitMQ

Verificar `RABBITMQ_URL` en `.env`:
```
RABBITMQ_URL=amqp://hexa:hexa@rabbit:5672/
```

### Tasks fallan silenciosamente

Revisar logs del worker y Redis (result backend):
```bash
docker compose -f compose.dev.yaml logs celery_worker
docker compose -f compose.dev.yaml exec redis redis-cli -a <password> keys "*celery*"
```

## Próximos Pasos

- [Service Locator](../architecture/04-service-locator.md) - Cómo llamar servicios desde tasks
- [Testing](../testing/05-service-tests.md) - Cómo testear tasks
