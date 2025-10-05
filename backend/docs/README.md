# Fast Hexagonal Backend Documentation

## Índice

1. [Inicio Rápido](./01-getting-started.md)
2. [Arquitectura del Proyecto](./02-architecture.md)
3. [Desarrollo de Nuevas Funcionalidades](./03-development-guide.md)
4. [Sistema de Dependencias](./04-dependency-injection.md)
5. [Roles y Permisos](./05-roles-permissions.md)
6. [Autenticación](./06-authentication.md)
7. [Módulos del Sistema](./modules/README.md)
8. [Descubrimiento de Módulos](./08-module-discovery.md)
9. [Service Locator](./09-service-locator.md)
10. [Inyección en Rutas](./10-route-injection.md)
11. [Buenas Prácticas](./11-best-practices.md)
12. [Tutorial Completo](./12-tutorial.md)

## Descripción General

Este proyecto implementa una **arquitectura hexagonal modular** con **FastAPI**, utilizando **dependency injection** y un sistema de **service locator** para la comunicación entre módulos.

### Características Principales

- ✅ **Arquitectura Hexagonal**: Separación clara entre dominio, aplicación e infraestructura
- ✅ **Modular**: Cada funcionalidad es un módulo independiente y portable
- ✅ **Dependency Injection**: Usando `dependency_injector` para gestión de dependencias
- ✅ **Service Locator**: Para comunicación entre módulos sin acoplamiento
- ✅ **Auto-discovery**: Los módulos se registran automáticamente
- ✅ **FastAPI**: API REST moderna con documentación automática
- ✅ **Roles y Permisos**: Sistema RBAC completo
- ✅ **Autenticación JWT**: Seguridad basada en tokens

### Tecnologías Utilizadas

- **FastAPI**: Framework web moderno
- **SQLAlchemy**: ORM para base de datos
- **dependency_injector**: Contenedor de inyección de dependencias
- **Alembic**: Migraciones de base de datos
- **Redis**: Cache y sesiones
- **JWT**: Autenticación basada en tokens
- **Pydantic**: Validación de datos

## Estructura del Proyecto

```
backend/
├── core/                    # Configuración y utilidades centrales
├── modules/                 # Módulos de negocio
│   ├── auth/               # Autenticación
│   ├── user/               # Gestión de usuarios
│   ├── rbac/               # Roles y permisos
│   └── ...                 # Otros módulos
├── shared/                 # Interfaces y utilidades compartidas
├── migrations/             # Migraciones de base de datos
└── docs/                   # Documentación
```

## Inicio Rápido

```bash
# Instalar dependencias
uv install

# Configurar variables de entorno
cp .env.example .env

# Ejecutar migraciones
alembic upgrade head

# Iniciar servidor de desarrollo
python -m hexa api --dev
```

Para más detalles, consulta la [Guía de Inicio](./01-getting-started.md).