# Inicio Rápido

## Requisitos Previos

- Python 3.11+
- uv (gestor de paquetes)
- PostgreSQL
- Redis

## Instalación

### 1. Clonar el repositorio

```bash
git clone <repository-url>
cd fast-hexagonal/backend
```

### 2. Instalar dependencias

```bash
uv install
```

### 3. Configurar variables de entorno

```bash
cp .env.example .env
```

Edita el archivo `.env` con tus configuraciones:

```env
# Base de datos
DATABASE_URL=postgresql://user:password@localhost/dbname

# Redis
REDIS_URL=redis://localhost:6379

# JWT
JWT_SECRET_KEY=your-secret-key
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30

# Configuración del servidor
BACKEND_PATH=/api
```

### 4. Ejecutar migraciones

```bash
alembic upgrade head
```

### 5. Iniciar el servidor

```bash
# Desarrollo
python -m hexa api --dev

# Producción
python -m hexa api
```

## Verificar la instalación

1. Abre tu navegador en `http://localhost:8000`
2. Ve a `http://localhost:8000/docs` para la documentación de la API
3. Verifica que los módulos se carguen correctamente en los logs

## Comandos útiles

```bash
# Crear una nueva migración
alembic revision --autogenerate -m "descripción"

# Aplicar migraciones
alembic upgrade head

# Revertir migración
alembic downgrade -1

# Limpiar cache
rm -rf .ruff_cache

# Ejecutar linter
ruff check .

# Formatear código
ruff format .
```

## Estructura de archivos importantes

```
backend/
├── .env                    # Variables de entorno
├── alembic.ini            # Configuración de migraciones
├── main.py                # Punto de entrada alternativo
├── hexa/                  # CLI principal
│   └── __main__.py
└── core/
    └── config/
        └── settings.py    # Configuración central
```

## Próximos pasos

- Lee la [Arquitectura del Proyecto](./02-architecture.md)
- Explora los [Módulos del Sistema](./07-modules.md)
- Sigue el [Tutorial Completo](./12-tutorial.md) para crear tu primer módulo