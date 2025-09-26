# Fast Hexagonal - Documentación

Sistema backend con arquitectura hexagonal desacoplada implementado en FastAPI.

## Índice de Documentación

### 📐 [Arquitectura](./architecture/)
- [Principios de Arquitectura Hexagonal](./architecture/hexagonal-principles.md)
- [Sistema de Desacoplamiento](./architecture/decoupling-system.md)
- [Inyección de Dependencias](./architecture/dependency-injection.md)
- [Patrones de Diseño](./architecture/design-patterns.md)

### 🧩 [Módulos](./modules/)
- [Estructura de Módulos](./modules/module-structure.md)
- [Módulos del Sistema](./modules/system-modules.md)
- [Módulos de Negocio](./modules/business-modules.md)

### 🚀 [Configuración](./setup/)
- [Instalación](./setup/installation.md)
- [Configuración del Entorno](./setup/environment.md)
- [Ejecución](./setup/running.md)

### 🔐 [RBAC](./rbac/)
- [Sistema de Roles](./rbac/roles.md)
- [Gestión de Permisos](./rbac/permissions.md)
- [Implementación](./rbac/implementation.md)

### ⚡ [Módulos Dinámicos](./dynamic-modules/)
- [Registro Automático](./dynamic-modules/auto-registration.md)
- [Comunicación Entre Módulos](./dynamic-modules/inter-module-communication.md)
- [Creación de Nuevos Módulos](./dynamic-modules/creating-modules.md)

### 📋 [Extras](./extras/)
- [API Reference](./extras/api-reference.md)
- [Guía de Migración](./extras/migration-guide.md)
- [Troubleshooting](./extras/troubleshooting.md)
- [Mejores Prácticas](./extras/best-practices.md)

## Características Principales

- ✅ **Arquitectura Hexagonal Pura**
- ✅ **Módulos Completamente Desacoplados**
- ✅ **Dependency Injection Automática**
- ✅ **Type-Safe Dependencies**
- ✅ **Sistema de Permisos Integrado**
- ✅ **Comando Único de Desarrollo**
- ✅ **49 Endpoints API Activos**
- ✅ **Testing Independiente por Módulo**

## Tecnologías

- **Framework**: FastAPI
- **Gestor de Dependencias**: uv
- **DI Container**: dependency-injector
- **ORM**: SQLAlchemy
- **Cache**: Redis
- **Base de Datos**: PostgreSQL/SQLite
- **Arquitectura**: Hexagonal + DDD + Dependency Injection

## Inicio Rápido

```bash
# Clonar repositorio
git clone <repository-url>
cd fast-hexagonal/backend

# Instalar dependencias
uv sync

# Ejecutar aplicación
uv run hexa dev

# Acceder a documentación
open http://localhost:8000/docs
```

## Módulos Activos

- **Authentication** (`/api/v1/auth`) - Login, registro, tokens
- **Users** (`/api/v1/users`) - Gestión de usuarios
- **RBAC** (`/api/v1/rbac`) - Roles y permisos
- **Finance** (`/api/v1/finance/currencies`) - Monedas
- **Providers** (`/api/v1/providers`) - Proveedores
- **Draft Invoices** (`/api/v1/providers/draft-invoices`) - Facturas
- **User Relationships** (`/api/v1/user-relationships`) - Relaciones
- **YiQi ERP** (`/api/v1/yiqi-erp`) - Integración ERP
- **Modules** (`/api/v1/modules`) - Información del sistema