# Fast Hexagonal - Documentación Completa

Bienvenido a la documentación del proyecto Fast Hexagonal, un backend modular construido con FastAPI siguiendo los principios de Arquitectura Hexagonal (Ports & Adapters).

## 📚 Índice de Documentación

### 🏗️ Arquitectura
- [**Visión General de la Arquitectura**](./architecture/01-overview.md) - Introducción a la arquitectura hexagonal del proyecto
- [**Estructura del Proyecto**](./architecture/02-project-structure.md) - Organización de carpetas y archivos
- [**Módulos y Desacoplamiento**](./architecture/03-modules.md) - Sistema de módulos independientes
- [**Service Locator Pattern**](./architecture/04-service-locator.md) - Comunicación entre módulos
- [**Dependency Injection**](./architecture/05-dependency-injection.md) - Containers y DI

### 🧩 Módulos
- [**Anatomía de un Módulo**](./modules/01-module-anatomy.md) - Estructura interna de un módulo
- [**Crear un Nuevo Módulo**](./modules/02-creating-module.md) - Guía paso a paso
- [**Auto-registro de Módulos**](./modules/03-module-registry.md) - Sistema de descubrimiento automático
- [**Módulos Existentes**](./modules/04-existing-modules.md) - Documentación de cada módulo

### ⚙️ Core
- [**Base de Datos**](./core/01-database.md) - SQLAlchemy, sesiones y transacciones
- [**FastAPI Server**](./core/02-fastapi-server.md) - Configuración y middlewares
- [**Celery**](./core/03-celery.md) - Sistema de tareas asíncronas
- [**Configuración**](./core/04-configuration.md) - Settings y variables de entorno
- [**Helpers y Utilities**](./core/05-helpers.md) - Utilidades compartidas

### 🔧 Desarrollo
- [**Inicio Rápido**](./development/01-quick-start.md) - Primeros pasos
- [**Docker Compose**](./development/02-docker-compose.md) - Desarrollo con Docker
- [**Comandos CLI**](./development/03-cli-commands.md) - Comandos disponibles en hexa
- [**Migraciones**](./development/04-migrations.md) - Alembic y gestión de DB
- [**Hot Reload**](./development/05-hot-reload.md) - Desarrollo con auto-recarga

### 🧪 Testing
- [**Estrategia de Testing**](./testing/01-strategy.md) - Tests unitarios, integración y e2e
- [**Configuración de Pytest**](./testing/02-pytest-config.md) - Fixtures y configuración
- [**Testing de Repositorios**](./testing/03-repository-tests.md) - Tests de integración con DB
- [**Testing de Use Cases**](./testing/04-usecase-tests.md) - Tests unitarios con mocks
- [**Testing de Servicios**](./testing/05-service-tests.md) - Tests de servicios

## 🚀 Inicio Rápido

```bash
# 1. Iniciar servicios
docker compose -f compose.dev.yaml up -d

# 2. Migrar base de datos
docker compose -f compose.dev.yaml exec backend uv run hexa migrate-db

# 3. Acceder a http://localhost:8000/api/docs
```

## 📖 Para Empezar

1. [Visión General de la Arquitectura](./architecture/01-overview.md)
2. [Estructura del Proyecto](./architecture/02-project-structure.md)
3. [Inicio Rápido](./development/01-quick-start.md)
4. [Crear un Nuevo Módulo](./modules/02-creating-module.md)

---

**Última actualización**: 2025-10-24
