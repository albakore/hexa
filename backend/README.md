# Fast Hexagonal Backend

Backend modular construido con **FastAPI** siguiendo **Arquitectura Hexagonal** (Ports & Adapters).

## 🚀 Inicio Rápido

```bash
# 1. Iniciar servicios
docker compose -f compose.dev.yaml up -d

# 2. Ejecutar migraciones
docker compose -f compose.dev.yaml exec backend alembic upgrade head

# 3. Acceder
open http://localhost:8000/api/docs
```

Ver [Guía Completa de Inicio](./docs/development/01-first-time-setup.md)

## 📚 Documentación

### Esenciales
- 📖 **[Documentación Completa](./docs/README.md)** - Índice principal
- 🚀 **[Inicio Rápido](./docs/QUICK_START.md)** - Empieza aquí
- 🏗️ **[Arquitectura](./docs/architecture/01-overview.md)** - Entiende el diseño
- ⚙️ **[Crear Módulo](./docs/modules/02-creating-module.md)** - Guía paso a paso

### Por Tema
- **Arquitectura**: [Visión General](./docs/architecture/01-overview.md) | [Estructura](./docs/architecture/02-project-structure.md) | [Service Locator](./docs/architecture/04-service-locator.md)
- **Desarrollo**: [Primera Vez](./docs/development/01-first-time-setup.md) | [Comandos CLI](./docs/development/03-cli-commands.md)
- **Core**: [Celery](./docs/core/03-celery.md)
- **Buenas Prácticas**: [Guía Completa](./docs/best-practices/BEST_PRACTICES.md)
- **Testing**: [Fix de Tests](./TESTING_REPOSITORY_FIX.md)

## 🏗️ Arquitectura

```
┌─────────────────────────────────────────┐
│           HTTP Request                   │
└────────────────┬────────────────────────┘
                 │
         ┌───────▼────────┐
         │  Input Adapter │  (FastAPI Router)
         └───────┬────────┘
                 │
         ┌───────▼────────┐
         │     Service    │  (Application Layer)
         └───────┬────────┘
                 │
         ┌───────▼────────┐
         │    Use Case    │  (Business Logic)
         └───────┬────────┘
                 │
         ┌───────▼────────┐
         │   Repository   │  (Port/Interface)
         └───────┬────────┘
                 │
         ┌───────▼────────┐
         │ Output Adapter │  (SQLAlchemy)
         └───────┬────────┘
                 │
         ┌───────▼────────┐
         │    Database    │
         └────────────────┘
```

## 🧩 Módulos

El proyecto está organizado en módulos independientes:

- **auth** - Autenticación y JWT
- **user** - Gestión de usuarios
- **rbac** - Roles y permisos
- **provider** - Proveedores
- **invoicing** - Facturación
- **finance** - Monedas
- **yiqi_erp** - Integración ERP
- **notifications** - Notificaciones

Cada módulo es autocontenido con su propio dominio, repositorios, servicios y APIs.

## 🔧 Stack Tecnológico

- **Framework**: FastAPI
- **ORM**: SQLAlchemy + SQLModel
- **Database**: PostgreSQL
- **Cache**: Redis
- **Queue**: Celery + RabbitMQ
- **Migration**: Alembic
- **Testing**: Pytest
- **DI**: dependency-injector
- **Package Manager**: uv

## 📦 Servicios Docker

```yaml
services:
  backend       # FastAPI (puerto 8000)
  celery_worker # Celery worker
  db            # PostgreSQL (puerto 5432)
  redis         # Redis (puerto 6379)
  rabbit        # RabbitMQ (puertos 5672, 15672)
  nginx         # Reverse proxy (puerto 80)
```

## 🎯 Comandos Útiles

```bash
# Ver logs
docker compose -f compose.dev.yaml logs -f backend

# Ejecutar tests
docker compose -f compose.dev.yaml exec backend pytest

# Crear migración
docker compose -f compose.dev.yaml exec backend alembic revision --autogenerate -m "descripción"

# Aplicar migraciones
docker compose -f compose.dev.yaml exec backend alembic upgrade head

# Shell Python
docker compose -f compose.dev.yaml exec backend python

# Ver comandos CLI
docker compose -f compose.dev.yaml exec backend uv run hexa --help
```

## 🧪 Testing

```bash
# Todos los tests
pytest

# Tests de un módulo
pytest modules/invoicing/test/

# Tests con coverage
pytest --cov=modules --cov-report=html

# Solo tests de integración
pytest -m integration
```

## 🔗 Accesos

- **API Docs**: http://localhost:8000/api/docs
- **RabbitMQ Management**: http://localhost:15672 (hexa/hexa)
- **PostgreSQL**: localhost:5432 (hexa/hexa/hexa)
- **Redis**: localhost:6379

## 📝 Crear un Módulo Nuevo

1. Crear estructura de carpetas en `modules/`
2. Definir entidad en `domain/entity/`
3. Definir repository interface en `domain/repository/`
4. Implementar repository en `adapter/output/persistence/`
5. Crear use cases en `domain/usecase/`
6. Crear service en `application/service/`
7. Crear container de DI en `container.py`
8. Crear endpoints en `adapter/input/api/v1/`
9. Crear `module.py` con registro
10. Crear migración de Alembic

Ver [Guía Completa](./docs/modules/02-creating-module.md)

## 🤝 Buenas Prácticas

- ✅ Usa nombres descriptivos
- ✅ Una responsabilidad por clase
- ✅ Lógica de negocio en use cases
- ✅ Service Locator para comunicación entre módulos
- ✅ Dependency Injection
- ✅ Tests con fixtures apropiadas

Ver [Guía de Buenas Prácticas](./docs/best-practices/BEST_PRACTICES.md)

## 📖 Aprende Más

- [Arquitectura Hexagonal](./docs/architecture/01-overview.md)
- [Service Locator Pattern](./docs/architecture/04-service-locator.md)
- [Sistema de Celery](./docs/core/03-celery.md)
- [Todas las Guías](./docs/README.md)

## 🐛 Troubleshooting

- **Módulos no aparecen**: Ver logs con `docker compose logs backend | grep module`
- **Celery no descubre tasks**: Verificar `RABBITMQ_URL` en `.env`
- **Tests fallan**: Ver [Testing Repository Fix](./TESTING_REPOSITORY_FIX.md)

## 📊 Estado del Proyecto

✅ **Funcional**
- Backend FastAPI con 11 módulos
- Celery worker con 3 tasks
- Auto-registro de módulos
- Hot reload para desarrollo
- Tests para módulo invoicing

⏳ **En Progreso**
- Tests para todos los módulos
- Documentación completa

## 📞 Soporte

- **Documentación**: [./docs/](./docs/)
- **Issues**: Crear issue en el repositorio
- **Changelog**: [CHANGELOG_SESSION.md](./CHANGELOG_SESSION.md)

---

**Última actualización**: 2025-10-24
