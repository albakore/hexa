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

## Tasks con Retry

```python
def process_invoice():
    """Task con retry automático"""
    try:
        # Lógica que puede fallar
        result = external_api.call()
        return result
    except Exception as e:
        # Celery manejará el retry automáticamente
        raise

# Para configurar retry, necesitas usar el decorador
# NOTA: Esto rompe el patrón actual. Mejor manejar retry en el dominio
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
