# Configuración del Entorno

## Variables de Entorno

### Core Settings
```bash
# .env
# Configuración básica de la aplicación
DEBUG=false
LOG_LEVEL=INFO
SECRET_KEY=your-super-secret-key-here
ENVIRONMENT=development

# Servidor
HOST=0.0.0.0
PORT=8000
RELOAD=false
WORKERS=1
```

### Base de Datos
```bash
# PostgreSQL (Producción)
DATABASE_URL=postgresql://username:password@localhost:5432/fast_hexagonal

# SQLite (Desarrollo)
DATABASE_URL=sqlite:///./db.sqlite

# Configuración adicional
DB_ECHO=false
DB_POOL_SIZE=5
DB_MAX_OVERFLOW=10
```

### Redis
```bash
# Configuración de Redis
REDIS_URL=redis://localhost:6379/0
REDIS_PASSWORD=
REDIS_DB=0
REDIS_MAX_CONNECTIONS=10

# Configuración de sesiones
SESSION_REDIS_DB=1
PERMISSION_REDIS_DB=2
```

### Autenticación JWT
```bash
# JWT Configuration
JWT_SECRET_KEY=your-jwt-secret-key
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7
```

### Módulos de Negocio

#### YiQi ERP
```bash
# YiQi ERP Integration
YIQI_BASE_URL=https://api.yiqi.com
YIQI_API_TOKEN=your-yiqi-api-token
YIQI_TIMEOUT=30
YIQI_RETRY_ATTEMPTS=3
```

#### Finance
```bash
# Finance Module
DEFAULT_CURRENCY=USD
EXCHANGE_RATE_PROVIDER=fixer.io
EXCHANGE_RATE_API_KEY=your-api-key
ACCOUNTING_PRECISION=2
```

#### File Storage
```bash
# File Storage (S3)
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_REGION=us-east-1
S3_BUCKET_NAME=your-bucket-name

# File Storage (Local)
LOCAL_STORAGE_PATH=./uploads
MAX_FILE_SIZE_MB=10
```

## Configuración por Entorno

### Desarrollo (.env.development)
```bash
DEBUG=true
LOG_LEVEL=DEBUG
RELOAD=true
DATABASE_URL=sqlite:///./dev.db
REDIS_URL=redis://localhost:6379/0

# Configuración relajada para desarrollo
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=1440  # 24 horas
CORS_ALLOW_ALL_ORIGINS=true
```

### Testing (.env.testing)
```bash
DEBUG=true
LOG_LEVEL=WARNING
DATABASE_URL=sqlite:///:memory:
REDIS_URL=redis://localhost:6379/15  # DB separada para tests

# Configuración para tests
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=5
DISABLE_AUTH=false  # Para tests de integración
```

### Staging (.env.staging)
```bash
DEBUG=false
LOG_LEVEL=INFO
DATABASE_URL=postgresql://user:pass@staging-db:5432/fast_hexagonal
REDIS_URL=redis://staging-redis:6379/0

# Configuración similar a producción
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
CORS_ALLOW_ALL_ORIGINS=false
CORS_ALLOWED_ORIGINS=["https://staging.yourapp.com"]
```

### Producción (.env.production)
```bash
DEBUG=false
LOG_LEVEL=WARNING
DATABASE_URL=postgresql://user:pass@prod-db:5432/fast_hexagonal
REDIS_URL=redis://prod-redis:6379/0

# Configuración de seguridad
SECRET_KEY=super-secure-secret-key
JWT_SECRET_KEY=super-secure-jwt-key
CORS_ALLOW_ALL_ORIGINS=false
CORS_ALLOWED_ORIGINS=["https://yourapp.com"]

# Performance
WORKERS=4
DB_POOL_SIZE=20
DB_MAX_OVERFLOW=30
```

## Configuración de Logging

### Configuración Básica
```python
# core/config/logging.py
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        },
        "detailed": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(module)s - %(funcName)s - %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "level": "INFO",
        },
        "file": {
            "class": "logging.FileHandler",
            "filename": "logs/app.log",
            "formatter": "detailed",
            "level": "DEBUG",
        },
    },
    "loggers": {
        "modules": {
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": False,
        },
        "uvicorn": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "WARNING",
    },
}
```

### Variables de Logging
```bash
# Logging Configuration
LOG_LEVEL=INFO
LOG_FORMAT=detailed
LOG_FILE=logs/app.log
LOG_MAX_SIZE=10MB
LOG_BACKUP_COUNT=5

# Logging por módulo
AUTH_LOG_LEVEL=DEBUG
USER_LOG_LEVEL=INFO
RBAC_LOG_LEVEL=WARNING
```

## Configuración de CORS

```bash
# CORS Configuration
CORS_ALLOW_ALL_ORIGINS=false
CORS_ALLOWED_ORIGINS=["http://localhost:3000", "https://yourapp.com"]
CORS_ALLOW_CREDENTIALS=true
CORS_ALLOWED_METHODS=["GET", "POST", "PUT", "DELETE", "OPTIONS"]
CORS_ALLOWED_HEADERS=["*"]
```

## Configuración de Middleware

```bash
# Middleware Configuration
ENABLE_RESPONSE_LOG=true
ENABLE_AUTHENTICATION=true
ENABLE_SQLALCHEMY_MIDDLEWARE=true

# Rate Limiting
RATE_LIMIT_ENABLED=true
RATE_LIMIT_REQUESTS_PER_MINUTE=60
RATE_LIMIT_BURST=10
```

## Configuración de Health Checks

```bash
# Health Check Configuration
HEALTH_CHECK_ENABLED=true
HEALTH_CHECK_INTERVAL=30
HEALTH_CHECK_TIMEOUT=5

# Checks específicos
DB_HEALTH_CHECK=true
REDIS_HEALTH_CHECK=true
EXTERNAL_API_HEALTH_CHECK=true
```

## Configuración de Métricas

```bash
# Metrics Configuration
METRICS_ENABLED=true
METRICS_PORT=9090
METRICS_PATH=/metrics

# Prometheus
PROMETHEUS_ENABLED=true
PROMETHEUS_NAMESPACE=fast_hexagonal
```

## Validación de Configuración

### Script de Validación
```python
# scripts/validate_config.py
import os
from typing import List, Tuple

def validate_config() -> List[Tuple[str, bool, str]]:
    """Valida la configuración del entorno"""
    checks = []
    
    # Variables requeridas
    required_vars = [
        "SECRET_KEY",
        "DATABASE_URL",
        "REDIS_URL",
        "JWT_SECRET_KEY"
    ]
    
    for var in required_vars:
        value = os.getenv(var)
        is_valid = value is not None and len(value) > 0
        message = "OK" if is_valid else "MISSING"
        checks.append((var, is_valid, message))
    
    # Validaciones específicas
    secret_key = os.getenv("SECRET_KEY", "")
    if len(secret_key) < 32:
        checks.append(("SECRET_KEY_LENGTH", False, "Too short (min 32 chars)"))
    else:
        checks.append(("SECRET_KEY_LENGTH", True, "OK"))
    
    return checks

if __name__ == "__main__":
    checks = validate_config()
    for var, is_valid, message in checks:
        status = "✅" if is_valid else "❌"
        print(f"{status} {var}: {message}")
```

### Comando de Validación
```bash
python scripts/validate_config.py
```

## Configuración de Docker

### docker-compose.yml
```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://postgres:password@db:5432/fast_hexagonal
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - db
      - redis
    env_file:
      - .env.production

  db:
    image: postgres:13
    environment:
      POSTGRES_DB: fast_hexagonal
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:6-alpine
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
```

### Variables de Docker
```bash
# Docker Configuration
DOCKER_REGISTRY=your-registry.com
DOCKER_IMAGE_TAG=latest
DOCKER_BUILD_TARGET=production
```

## Configuración de Monitoreo

```bash
# Monitoring Configuration
SENTRY_DSN=https://your-sentry-dsn
SENTRY_ENVIRONMENT=production
SENTRY_TRACES_SAMPLE_RATE=0.1

# APM
NEW_RELIC_LICENSE_KEY=your-license-key
NEW_RELIC_APP_NAME=fast-hexagonal-api
```

## Mejores Prácticas

### 1. Seguridad
- Nunca commitear archivos `.env`
- Usar secretos seguros (mínimo 32 caracteres)
- Rotar claves regularmente
- Usar variables específicas por entorno

### 2. Organización
- Agrupar variables por funcionalidad
- Documentar variables complejas
- Usar valores por defecto sensatos
- Validar configuración al inicio

### 3. Desarrollo
- Usar `.env.example` como plantilla
- Configuración relajada para desarrollo
- Base de datos en memoria para tests
- Logging detallado en desarrollo