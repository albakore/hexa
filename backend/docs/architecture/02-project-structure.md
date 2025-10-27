# Estructura del Proyecto

## Vista General

```
backend/
├── core/                    # Funcionalidad compartida del core
├── hexa/                    # CLI commands
├── modules/                 # Módulos de negocio
├── shared/                  # Código compartido entre módulos
├── migrations/              # Migraciones de Alembic
├── docker/                  # Dockerfiles
├── docs/                    # Documentación
├── .env                     # Variables de entorno
├── compose.dev.yaml         # Docker Compose para desarrollo
├── pyproject.toml          # Configuración del proyecto
└── uv.lock                 # Lock de dependencias
```

## /core - Funcionalidad Core

```
core/
├── celery/                 # Sistema de Celery
│   ├── config.py          # Configuración de Celery
│   └── discovery.py       # Descubrimiento de tasks
├── db/                     # Base de datos
│   ├── session.py         # Sesiones de SQLAlchemy
│   ├── transactional.py   # Decorador @Transactional
│   └── redis_db.py        # Cliente Redis
├── fastapi/               # FastAPI configuration
│   ├── server/            # Creación de app
│   │   └── __init__.py    # create_app(), lifespan
│   ├── middlewares/       # Middlewares
│   │   ├── authentication.py
│   │   ├── sqlalchemy.py
│   │   └── response_log.py
│   └── dependencies/      # Dependencies de FastAPI
│       ├── permission.py
│       └── user_permission/
├── config/                # Configuración
│   └── settings.py        # Pydantic Settings
├── helpers/               # Utilidades
│   ├── token.py          # JWT tokens
│   └── password.py       # Hashing de passwords
└── exceptions/            # Excepciones base
    └── base.py
```

### core/celery/

**discovery.py**: Crea el worker y descubre tasks automáticamente
```python
def create_celery_worker() -> Celery:
    # 1. Crea app de Celery
    # 2. Busca servicios que terminan en "_tasks" en service_locator
    # 3. Registra cada función como task
    # 4. Retorna app configurada
```

**config.py**: Configuración de Celery (broker, backend, etc.)

### core/db/

**session.py**: 
- `session_factory()` - Crea sesiones de SQLAlchemy
- `session` - async_scoped_session para contextos
- `set_session_context()` / `reset_session_context()` - Manejo de contextos

**transactional.py**: Decorador `@Transactional` para manejar transacciones automáticamente

**redis_db.py**: Cliente Redis configurado

### core/fastapi/

**server/__init__.py**: Punto de entrada de FastAPI
- `create_app()` - Crea y configura la aplicación
- `lifespan()` - Maneja startup/shutdown
- `init_routes_pack()` - Monta rutas de módulos
- `make_middleware()` - Configura middlewares

**middlewares/**: 
- `SQLAlchemyMiddleware` - Maneja sesiones por request
- `AuthenticationMiddleware` - Autenticación JWT
- `ResponseLogMiddleware` - Logging de responses

**dependencies/**:
- `permission.py` - Sistema de permisos
- `user_permission/` - Verificación de permisos de usuario

### core/config/

**settings.py**: Configuración con Pydantic BaseSettings
```python
class Settings(BaseSettings):
    DATABASE_URL: str
    REDIS_URL: str
    RABBITMQ_URL: str
    JWT_SECRET_KEY: str
    # ...
```

## /hexa - CLI Commands

```
hexa/
└── __main__.py          # Todos los comandos CLI
```

**Comandos disponibles**:
- `api` - Inicia FastAPI server
- `celery-apps` - Inicia Celery worker
- `migrate-db` - Ejecuta migraciones pendientes
- `create-migration` - Crea nueva migración
- `shell` - Shell interactivo Python
- `test-celery` - Prueba Celery

Ver más en [Comandos CLI](../development/03-cli-commands.md)

## /modules - Módulos de Negocio

```
modules/
├── auth/                    # Autenticación
├── user/                    # Usuarios
├── rbac/                    # Roles y permisos
├── provider/                # Proveedores
├── invoicing/              # Facturación
├── finance/                # Monedas y finanzas
├── yiqi_erp/              # Integración ERP
├── notifications/          # Notificaciones
├── file_storage/          # Almacenamiento de archivos
├── user_relationships/    # Relaciones entre usuarios
└── module/                # Módulos de la app

Cada módulo tiene esta estructura:
├── domain/                 # Dominio puro
│   ├── entity/            # Entidades
│   ├── repository/        # Interfaces (ports)
│   ├── usecase/          # Casos de uso
│   └── vo/               # Value Objects (opcional)
├── application/           # Capa de aplicación
│   ├── service/          # Servicios de aplicación
│   ├── dto/              # Data Transfer Objects
│   └── command/          # Commands (opcional)
├── adapter/              # Adaptadores
│   ├── input/           # Adaptadores de entrada
│   │   ├── api/         # Endpoints HTTP
│   │   │   └── v1/      # Versión 1 de la API
│   │   ├── tasks/       # Tareas Celery
│   │   └── cli/         # Comandos CLI (opcional)
│   └── output/          # Adaptadores de salida
│       ├── persistence/ # Repositorios
│       │   └── sqlalchemy/  # Implementación SQLAlchemy
│       ├── api/         # Clientes HTTP externos
│       └── cache/       # Caché (opcional)
├── test/                # Tests del módulo
│   ├── conftest.py     # Fixtures
│   ├── test_*_repository.py
│   ├── test_*_usecase.py
│   └── test_*_service.py
├── container.py         # Dependency Injection Container
└── module.py           # Registro del módulo
```

## /shared - Código Compartido

```
shared/
└── interfaces/              # Interfaces compartidas
    ├── module_discovery.py  # Descubrimiento de módulos
    ├── module_registry.py   # Registro de módulos
    ├── service_locator.py   # Service Locator
    ├── module_contracts.py  # Contratos entre módulos
    └── service_protocols.py # Protocols para servicios
```

**module_discovery.py**: 
- `discover_modules()` - Escanea y registra módulos automáticamente

**module_registry.py**:
- `ModuleRegistry` - Singleton que mantiene todos los módulos
- `ModuleInterface` - Interface que deben implementar los módulos

**service_locator.py**:
- `ServiceLocator` - Registro de servicios para comunicación entre módulos
- `service_locator` - Instancia global

## /migrations - Alembic Migrations

```
migrations/
├── versions/           # Archivos de migración
│   ├── 001_initial.py
│   ├── 002_add_users.py
│   └── ...
├── env.py             # Configuración de Alembic
├── script.py.mako     # Template para migraciones
└── alembic.ini        # Configuración Alembic (en raíz)
```

## /docker - Dockerfiles

```
docker/
├── hexa/
│   ├── dev.Dockerfile     # Imagen para desarrollo
│   └── prod.Dockerfile    # Imagen para producción
└── nginx/
    └── nginx.conf        # Configuración nginx
```

## Archivos de Configuración Raíz

### compose.dev.yaml
Docker Compose para desarrollo con:
- **backend**: FastAPI con hot-reload
- **celery_worker**: Con watchfiles
- **db (postgres)**: PostgreSQL 15
- **redis**: Redis 6.2
- **rabbit**: RabbitMQ 4
- **nginx**: Reverse proxy

### .env
Variables de entorno:
```bash
DATABASE_URL=postgresql+asyncpg://hexa:hexa@postgres:5432/hexa
REDIS_URL=redis://redis:6379/0
RABBITMQ_URL=amqp://hexa:hexa@rabbit:5672/
JWT_SECRET_KEY=your-secret-key
# ...
```

### pyproject.toml
Configuración del proyecto:
- Dependencias
- Scripts
- Configuración de pytest
- Configuración de ruff/mypy

### uv.lock
Lock file de dependencias (generado por uv)

## Flujo de Archivos en una Request

```
1. HTTP Request → nginx:80

2. nginx → backend:8000 (/api/*)

3. core/fastapi/server/__init__.py
   ↓ create_app() ya ejecutado
   ↓ Módulos ya registrados

4. core/fastapi/middlewares/sqlalchemy.py
   ↓ Crea sesión de DB

5. modules/{module}/adapter/input/api/v1/{endpoint}.py
   ↓ Router de FastAPI

6. modules/{module}/application/service/{service}.py
   ↓ Application Service

7. modules/{module}/domain/usecase/{usecase}.py
   ↓ Use Case (lógica de negocio)

8. modules/{module}/adapter/output/persistence/{adapter}.py
   ↓ Repository Adapter

9. modules/{module}/adapter/output/persistence/sqlalchemy/{repo}.py
   ↓ Implementación SQLAlchemy

10. core/db/session.py
    ↓ global_session

11. PostgreSQL Database

12. Response ← ← ← ← (hacia arriba por todas las capas)
```

## Convenciones de Nombres de Archivos

### Entidades
`{entity_name}.py` - Singular, snake_case
- `purchase_invoice.py`
- `user.py`
- `provider.py`

### Repositories
`{entity_name}.py` en `domain/repository/`
- `purchase_invoice.py` (interface)

`{entity_name}.py` en `adapter/output/persistence/sqlalchemy/`
- `purchase_invoice.py` (implementación)

### Services
`{entity_name}.py` en `application/service/`
- `purchase_invoice.py`
- `user.py`

### Use Cases
`{entity_name}.py` en `domain/usecase/`
- `purchase_invoice.py` (contiene varios use cases)

### API Endpoints
`{entity_name}.py` en `adapter/input/api/v1/`
- `purchase_invoice.py`
- `user.py`

### Tasks
`{entity_name}.py` en `adapter/input/tasks/`
- `invoice.py`
- `notification.py`

## Próximo Paso

Lee [Sistema de Módulos](./03-modules.md) para entender cómo funcionan los módulos.
