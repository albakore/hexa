# Comandos CLI - hexa

El proyecto incluye un CLI construido con Typer que proporciona comandos para gestionar el proyecto.

## Uso General

```bash
# Ver todos los comandos
uv run hexa --help

# En Docker
docker compose -f compose.dev.yaml exec backend uv run hexa --help
```

## Comandos Disponibles

### `api` - Iniciar FastAPI Server

Inicia el servidor FastAPI.

```bash
# Modo normal
uv run hexa api

# Modo desarrollo (con hot-reload)
uv run hexa api --dev
```

**Opciones**:
- `--dev`: Activa hot-reload con uvicorn

**Configuración**:
- Puerto: 8000
- Host: 0.0.0.0
- Root path: Definido en `BACKEND_PATH` (.env)

**Uso en Docker**:
```yaml
# compose.dev.yaml
backend:
  command: /bin/sh -c "uv run hexa api --dev"
```

---

### `celery-apps` - Iniciar Celery Worker

Inicia el worker de Celery con todas las tasks descubiertas automáticamente.

```bash
uv run hexa celery-apps
```

**Qué hace**:
1. Limpia `ModuleRegistry` y `service_locator` (para hot-reload)
2. Descubre todos los módulos con `discover_modules()`
3. Crea worker de Celery con `create_celery_worker()`
4. Inicia worker con loglevel INFO

**Salida esperada**:
```
🔍 Discovering and registering modules...
✅ Found invoicing module
✅ Found user module
...
📦 Discovered 3 task services from service_locator
  ✓ Registered: invoicing.emit_invoice
  ✓ Registered: notifications.send_notification
  ✓ Registered: yiqi_erp.emit_invoice

✅ Total 3 tasks registered in Celery worker
```

**Uso en Docker**:
```yaml
# compose.dev.yaml (con hot-reload)
celery_worker:
  command: /bin/sh -c "uv run watchfiles --filter python 'uv run hexa celery-apps' modules core shared"
```

---

### `test-celery` - Probar Celery

Envía tasks de prueba a Celery para verificar que funciona.

```bash
uv run hexa test-celery
```

**Qué hace**:
1. Obtiene tasks desde `service_locator`:
   - `invoicing_tasks`
   - `yiqi_erp_tasks`
   - `notifications_tasks`
2. Ejecuta cada task con `.delay()`

**Salida esperada**:
```
✅ Task de invoicing enviada
✅ Task de yiqi_erp enviada  
✅ Task de notifications enviada

📤 Se enviaron todas las tareas de prueba
```

**Verificar ejecución**:
```bash
# Ver logs del worker
docker compose -f compose.dev.yaml logs -f celery_worker
```

---

### `delete-alembic-version` - Borrar Versión de Alembic

Elimina el registro de la tabla `alembic_version`. Útil cuando necesitas resetear migraciones.

```bash
uv run hexa delete-alembic-version
```

**⚠️ Advertencia**: Esto borrará el tracking de migraciones. Úsalo solo si sabes lo que haces.

**Qué hace**:
```sql
DELETE FROM alembic_version;
```

**Cuándo usarlo**:
- Cuando quieres volver a ejecutar todas las migraciones desde cero
- Cuando tienes conflictos de migraciones
- En desarrollo, para resetear el estado

---

### `makeuser` - Crear Usuario

Comando para crear un usuario (pendiente de implementación).

```bash
uv run hexa makeuser
```

**Estado**: TODO - No implementado aún

---

## Comandos de Migraciones (Alembic)

Aunque no están en `hexa/__main__.py`, estos comandos de Alembic son importantes:

### Crear Nueva Migración

```bash
# Autogenerar basándose en cambios en modelos
docker compose -f compose.dev.yaml exec backend alembic revision --autogenerate -m "descripción"

# Crear migración vacía
docker compose -f compose.dev.yaml exec backend alembic revision -m "descripción"
```

### Aplicar Migraciones

```bash
# Aplicar todas las pendientes
docker compose -f compose.dev.yaml exec backend alembic upgrade head

# Aplicar hasta una versión específica
docker compose -f compose.dev.yaml exec backend alembic upgrade <revision>

# Aplicar siguiente migración
docker compose -f compose.dev.yaml exec backend alembic upgrade +1
```

### Ver Estado de Migraciones

```bash
# Ver historial
docker compose -f compose.dev.yaml exec backend alembic history

# Ver versión actual
docker compose -f compose.dev.yaml exec backend alembic current

# Ver migraciones pendientes
docker compose -f compose.dev.yaml exec backend alembic show head
```

### Revertir Migraciones

```bash
# Revertir última migración
docker compose -f compose.dev.yaml exec backend alembic downgrade -1

# Revertir todas
docker compose -f compose.dev.yaml exec backend alembic downgrade base

# Revertir hasta versión específica
docker compose -f compose.dev.yaml exec backend alembic downgrade <revision>
```

---

## Crear Comandos Personalizados

Para agregar un nuevo comando al CLI:

```python
# hexa/__main__.py

@cmd.command("mi-comando")
def mi_comando(
    argumento: str,
    opcion: bool = False
):
    """Descripción del comando"""
    if opcion:
        print(f"Ejecutando con: {argumento}")
    else:
        print("Modo normal")

# Uso:
# uv run hexa mi-comando "valor" --opcion
```

**Tipos de argumentos**:
```python
@cmd.command()
def ejemplo(
    requerido: str,                    # Argumento requerido
    opcional: str = "default",         # Argumento opcional con default
    flag: bool = False,                # Flag boolean
    numero: int = 10,                  # Argumento numérico
    opciones: str = typer.Option(...), # Opción con typer
):
    pass
```

---

## Ejecutar Python Code Directo

### Shell Interactivo

```bash
docker compose -f compose.dev.yaml exec backend python

>>> from core.db import session
>>> from modules.user.domain.entity.user import User
>>> async with session() as s:
...     users = await s.execute(select(User))
...     print(users.scalars().all())
```

### Script One-liner

```bash
docker compose -f compose.dev.yaml exec backend python -c "
from core.db import session
print('Hello from Python!')
"
```

---

## Comandos Útiles Combinados

### Reiniciar Servicios

```bash
# Reiniciar backend y celery
docker compose -f compose.dev.yaml restart backend celery_worker

# Ver logs en tiempo real
docker compose -f compose.dev.yaml logs -f backend celery_worker
```

### Debugging

```bash
# Entrar al container
docker compose -f compose.dev.yaml exec backend bash

# Ver procesos
docker compose -f compose.dev.yaml exec backend ps aux

# Ver variables de entorno
docker compose -f compose.dev.yaml exec backend env | grep -E "(DATABASE|REDIS|RABBIT)"
```

### Tests

```bash
# Todos los tests
docker compose -f compose.dev.yaml exec backend pytest

# Tests de un módulo
docker compose -f compose.dev.yaml exec backend pytest modules/invoicing/test/

# Tests con coverage
docker compose -f compose.dev.yaml exec backend pytest --cov=modules --cov-report=html

# Tests solo de integración
docker compose -f compose.dev.yaml exec backend pytest -m integration

# Tests solo unitarios
docker compose -f compose.dev.yaml exec backend pytest -m unit
```

---

## Troubleshooting

### Comando no funciona

```bash
# Verificar que estás en el directorio correcto
pwd
# Debe terminar en /backend

# Verificar que hexa existe
ls hexa/__main__.py

# Ejecutar directamente con Python
python -m hexa --help
```

### Error "Module not found"

```bash
# Verificar PYTHONPATH
export PYTHONPATH=/app:$PYTHONPATH

# O ejecutar desde raíz del proyecto
cd /path/to/backend
uv run hexa --help
```

### Worker de Celery no descubre tasks

1. Verificar que módulos están registrados:
```bash
docker compose logs backend | grep "Found.*module"
```

2. Verificar que tasks están en service_locator:
```bash
docker compose logs celery_worker | grep "Registered"
```

3. Reiniciar worker:
```bash
docker compose restart celery_worker
```

---

## Próximos Pasos

- [Migraciones de Base de Datos](./04-migrations.md)
- [Hot Reload](./05-hot-reload.md)
- [Docker Compose](./02-docker-compose.md)
