# Configuración Inicial del Proyecto

## Requisitos Previos

- **Docker** y **Docker Compose** instalados
- **Git** para clonar el repositorio
- (Opcional) **Python 3.11+** y **uv** para desarrollo local

## Paso 1: Clonar el Repositorio

```bash
git clone <repository-url>
cd fast-hexagonal/backend
```

## Paso 2: Configurar Variables de Entorno

```bash
# Copiar el archivo de ejemplo
cp .env.example .env

# Editar si es necesario
nano .env
```

**Variables importantes**:
```bash
# Base de datos
DATABASE_URL=postgresql+asyncpg://hexa:hexa@postgres:5432/hexa

# Redis
REDIS_URL=redis://redis:6379/0
REDIS_PASSWORD=eYVX7EwVmmxKPCDmwMtyKVge8oLd2t81

# RabbitMQ
RABBITMQ_URL=amqp://hexa:hexa@rabbit:5672/

# JWT
JWT_SECRET_KEY=omelettedufromage  # ⚠️ Cambiar en producción
JWT_ALGORITHM=HS256

# Paths
BACKEND_PATH=/api
```

## Paso 3: Iniciar Servicios con Docker Compose

```bash
# Iniciar todos los servicios en background
docker compose -f compose.dev.yaml up -d

# Ver logs para verificar que todo inició correctamente
docker compose -f compose.dev.yaml logs -f
```

**Servicios que se iniciarán**:
- `backend` - FastAPI (puerto 8000)
- `celery_worker` - Celery worker
- `db` (postgres) - PostgreSQL (puerto 5432)
- `redis` - Redis (puerto 6379)
- `rabbit` (rabbitmq) - RabbitMQ (puertos 5672, 15672)
- `nginx` - Reverse proxy (puerto 80)

**Verificar estado**:
```bash
docker compose -f compose.dev.yaml ps

# Deberías ver:
# NAME             STATUS                   PORTS
# backend          Up                       0.0.0.0:8000->8000/tcp
# backend-celery   Up                       
# postgres         Up (healthy)             0.0.0.0:5432->5432/tcp
# redis            Up (healthy)             0.0.0.0:6379->6379/tcp
# rabbitmq         Up (healthy)             0.0.0.0:5672->5672/tcp, 0.0.0.0:15672->15672/tcp
# nginx            Up                       0.0.0.0:80->80/tcp
```

## Paso 4: Crear Base de Datos (Primera Vez)

```bash
# Conectarse al container de PostgreSQL
docker compose -f compose.dev.yaml exec db psql -U hexa

# Crear base de datos si no existe
CREATE DATABASE hexa;

# Salir
\q
```

**Nota**: Si el DATABASE_URL está correctamente configurado, la base de datos debería crearse automáticamente.

## Paso 5: Ejecutar Migraciones

```bash
# Aplicar todas las migraciones
docker compose -f compose.dev.yaml exec backend alembic upgrade head
```

**Salida esperada**:
```
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> 001, initial migration
INFO  [alembic.runtime.migration] Running upgrade 001 -> 002, add users
...
```

**Verificar tablas creadas**:
```bash
docker compose -f compose.dev.yaml exec db psql -U hexa -d hexa -c "\dt"

# Deberías ver:
#  Schema |       Name        | Type  | Owner
# --------+-------------------+-------+-------
#  public | alembic_version   | table | hexa
#  public | user              | table | hexa
#  public | purchaseinvoice   | table | hexa
#  ...
```

## Paso 6: Verificar que Todo Funciona

### 6.1 Verificar Backend FastAPI

```bash
# Ver logs del backend
docker compose -f compose.dev.yaml logs backend | grep "module"

# Deberías ver:
# ✅ Found auth module
# ✅ Found invoicing module
# ✅ Found user module
# ...
# 📦 Total 11 modules installed
```

**Acceder a la documentación**:
- Abrir: http://localhost:8000/api/docs
- Deberías ver Swagger UI con todos los endpoints de los módulos

### 6.2 Verificar Celery Worker

```bash
# Ver logs del worker
docker compose -f compose.dev.yaml logs celery_worker | grep -E "(Registered|tasks registered)"

# Deberías ver:
# ✓ Registered: invoicing.emit_invoice
# ✓ Registered: notifications.send_notification
# ✓ Registered: yiqi_erp.emit_invoice
# ✅ Total 3 tasks registered in Celery worker
```

**Probar Celery**:
```bash
docker compose -f compose.dev.yaml exec backend uv run hexa test-celery

# Deberías ver:
# ✅ Task de invoicing enviada
# ✅ Task de yiqi_erp enviada
# ✅ Task de notifications enviada
```

### 6.3 Verificar RabbitMQ

- Abrir: http://localhost:15672
- Login: `hexa` / `hexa`
- Ir a "Queues" y verificar que existe la queue `celery`

### 6.4 Verificar PostgreSQL

```bash
# Conectarse a la base de datos
docker compose -f compose.dev.yaml exec db psql -U hexa -d hexa

# Contar registros de una tabla
SELECT COUNT(*) FROM purchaseinvoice;

# Salir
\q
```

### 6.5 Verificar Redis

```bash
# Conectarse a Redis
docker compose -f compose.dev.yaml exec redis redis-cli -a eYVX7EwVmmxKPCDmwMtyKVge8oLd2t81

# Verificar conectividad
PING
# Debería responder: PONG

# Ver keys
KEYS *

# Salir
exit
```

## Paso 7: Ejecutar Tests (Opcional)

```bash
# Ejecutar todos los tests
docker compose -f compose.dev.yaml exec backend pytest

# Ejecutar tests de un módulo específico
docker compose -f compose.dev.yaml exec backend pytest modules/invoicing/test/

# Con cobertura
docker compose -f compose.dev.yaml exec backend pytest --cov=modules --cov-report=html
```

## Troubleshooting Común

### Error: "Connection refused" al conectar a PostgreSQL

**Solución**: Esperar a que PostgreSQL termine de iniciar
```bash
# Verificar logs
docker compose -f compose.dev.yaml logs db

# Esperar a ver: "database system is ready to accept connections"

# Reiniciar backend
docker compose -f compose.dev.yaml restart backend
```

### Error: "Module 'X' already registered"

**Solución**: Limpiar y reiniciar
```bash
docker compose -f compose.dev.yaml down
docker compose -f compose.dev.yaml up -d
```

### Error: Celery no encuentra tasks

**Solución**: Verificar RABBITMQ_URL en .env
```bash
# Debe ser:
RABBITMQ_URL=amqp://hexa:hexa@rabbit:5672/

# NO debe ser:
RABBITMQ_URL=amqp://hexa:hexa@localhost:5672/  # ❌
```

### Error: Redis healthcheck failed

**Solución**: Limpiar volumen de Redis
```bash
docker compose -f compose.dev.yaml down
docker volume rm fast-hexagonal_redis
docker compose -f compose.dev.yaml up -d redis
```

### No aparecen módulos en /docs

**Solución**: Verificar que módulos se registraron
```bash
docker compose -f compose.dev.yaml logs backend | grep "Found.*module"

# Si no aparece nada, reiniciar:
docker compose -f compose.dev.yaml restart backend
```

## Comandos Útiles Post-Setup

```bash
# Ver todos los logs
docker compose -f compose.dev.yaml logs -f

# Ver logs de un servicio específico
docker compose -f compose.dev.yaml logs -f backend
docker compose -f compose.dev.yaml logs -f celery_worker

# Reiniciar un servicio
docker compose -f compose.dev.yaml restart backend

# Parar todos los servicios
docker compose -f compose.dev.yaml down

# Parar y eliminar volúmenes
docker compose -f compose.dev.yaml down -v

# Rebuil y reiniciar
docker compose -f compose.dev.yaml up -d --build
```

## Siguiente Paso

Ahora que tienes el proyecto funcionando:

1. Lee [Docker Compose](./02-docker-compose.md) para entender la configuración
2. Explora [Comandos CLI](./03-cli-commands.md) disponibles
3. Aprende sobre [Hot Reload](./05-hot-reload.md) para desarrollo
4. Crea tu primer módulo siguiendo [Crear un Módulo](../modules/02-creating-module.md)

## Accesos Rápidos

- **API Docs**: http://localhost:8000/api/docs
- **RabbitMQ**: http://localhost:15672 (hexa/hexa)
- **PostgreSQL**: localhost:5432 (hexa/hexa/hexa)
- **Redis**: localhost:6379 (pass: eYVX7EwVmmxKPCDmwMtyKVge8oLd2t81)
