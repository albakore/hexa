# Guía de Inicio Rápido

## Requisitos

- Docker y Docker Compose
- Git

## 1. Primer Inicio

```bash
# Clonar y entrar al proyecto
cd fast-hexagonal/backend

# Copiar variables de entorno
cp .env.example .env

# Levantar servicios
docker compose -f compose.dev.yaml up -d

# Ver logs
docker compose -f compose.dev.yaml logs -f backend

# Esperar a ver: "✅ Modules registered"
```

## 2. Migrar Base de Datos

```bash
# Primera vez: crear la base de datos
docker compose -f compose.dev.yaml exec backend uv run hexa migrate-db

# Ver tablas creadas
docker compose -f compose.dev.yaml exec db psql -U hexa -d hexa -c "\dt"
```

## 3. Acceder a la Aplicación

- **API Docs**: http://localhost:8000/api/docs
- **RabbitMQ Management**: http://localhost:15672 (user: hexa, pass: hexa)
- **Database**: localhost:5432 (user: hexa, pass: hexa, db: hexa)

## 4. Comandos Útiles

```bash
# Ver todos los comandos disponibles
docker compose -f compose.dev.yaml exec backend uv run hexa --help

# Ejecutar tests
docker compose -f compose.dev.yaml exec backend pytest

# Shell interactivo
docker compose -f compose.dev.yaml exec backend uv run hexa shell

# Ver módulos registrados
docker compose -f compose.dev.yaml logs backend | grep "Found.*module"
```

## 5. Estructura de Módulos

El proyecto está organizado en módulos independientes:

- **auth**: Autenticación y JWT
- **user**: Gestión de usuarios
- **rbac**: Roles y permisos
- **provider**: Proveedores
- **invoicing**: Facturación
- **finance**: Monedas y finanzas
- **yiqi_erp**: Integración con ERP externo

## 6. Crear un Nuevo Módulo

Ver [Crear un Nuevo Módulo](./modules/02-creating-module.md)

## 7. Hot Reload

El proyecto está configurado con auto-reload:

- **Backend FastAPI**: Se recarga automáticamente al cambiar archivos Python
- **Celery Worker**: Se recarga con `watchfiles` al cambiar archivos en `modules/`, `core/`, `shared/`

## 8. Troubleshooting

### No veo mis rutas en /docs

El backend debe mostrar al iniciar:
```
✅ Found invoicing module
✅ Found user module
...
```

Si no aparecen, revisar logs: `docker compose -f compose.dev.yaml logs backend`

### Celery no encuentra las tasks

Ver logs de celery_worker:
```bash
docker compose -f compose.dev.yaml logs celery_worker

# Deberías ver:
# ✅ Total 3 tasks registered in Celery worker
#   . invoicing.emit_invoice
#   . notifications.send_notification
#   . yiqi_erp.emit_invoice
```

### Error de conexión a base de datos

```bash
# Verificar que postgres está healthy
docker compose -f compose.dev.yaml ps

# Reiniciar si es necesario
docker compose -f compose.dev.yaml restart db backend
```

## Próximos Pasos

- Lee [Arquitectura del Proyecto](./architecture/01-overview.md)
- Entiende [Cómo funcionan los Módulos](./modules/01-module-anatomy.md)
- Aprende sobre [Service Locator](./architecture/04-service-locator.md)
- Crea tu [Primer Módulo](./modules/02-creating-module.md)
