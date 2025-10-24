# Variables de Entorno - Configuración para Producción

## Variables Requeridas

### Base de Datos
```bash
DATABASE_URL=postgresql+asyncpg://usuario:password@host:5432/nombre_db

# Ejemplo Producción
DATABASE_URL=postgresql+asyncpg://hexa_prod:SecurePass123@db.production.com:5432/hexa_prod

# Pool de conexiones (opcional)
DB_POOL_SIZE=20
DB_MAX_OVERFLOW=10
```

### Redis
```bash
REDIS_URL=redis://host:6379/db_number
REDIS_PASSWORD=tu_password_redis

# Ejemplo Producción
REDIS_URL=redis://redis.production.com:6379/0
REDIS_PASSWORD=SuperSecureRedisPassword123
```

### RabbitMQ
```bash
RABBITMQ_URL=amqp://usuario:password@host:5672/vhost

# Ejemplo Producción
RABBITMQ_URL=amqp://hexa_prod:SecurePass123@rabbitmq.production.com:5672/hexa_vhost
```

### JWT
```bash
JWT_SECRET_KEY=tu_clave_secreta_muy_larga_y_segura
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=30

# ⚠️ IMPORTANTE: Usar una clave segura diferente en cada ambiente
# Generar con: python -c "import secrets; print(secrets.token_urlsafe(64))"
```

### Paths
```bash
BACKEND_PATH=/api
FRONTEND_URL=https://tu-frontend.com
BACKEND_URL=https://api.tu-dominio.com
```

### Integraciones Externas

#### Yiqi ERP
```bash
YIQI_BASE_URL=https://api.yiqi.com.ar
YIQI_API_TOKEN=tu_token_de_yiqi
YIQI_LAST_INVOICE_UPDATE=[2025,1,1]
YIQI_ENV=produccion_id
```

#### Email (SMTP)
```bash
EMAIL_SMTP_SERVER=smtp.tu-proveedor.com
EMAIL_SMTP_PORT=587
EMAIL_SMTP_APPLICATION=nombre-app
EMAIL_SMTP_MAILSENDER=noreply@tu-dominio.com
EMAIL_SMTP_USERNAME=smtp_usuario
EMAIL_SMTP_PASSWORD=smtp_password
```

#### AWS S3
```bash
AWS_ACCESS_KEY=AKIAIOSFODNN7EXAMPLE
AWS_ACCESS_SECRET_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
AWS_ACCESS_REGION=us-east-1
AWS_ACCESS_BUCKET_NAME=nombre-bucket-produccion
```

### Otros
```bash
COMPOSE_PROJECT_NAME=fast-hexagonal-prod
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=INFO
```

## Configuración por Ambiente

### Desarrollo (.env.dev)
```bash
DATABASE_URL=postgresql+asyncpg://hexa:hexa@postgres:5432/hexa
REDIS_URL=redis://redis:6379/0
REDIS_PASSWORD=eYVX7EwVmmxKPCDmwMtyKVge8oLd2t81
RABBITMQ_URL=amqp://hexa:hexa@rabbit:5672/
JWT_SECRET_KEY=omelettedufromage  # OK para desarrollo
ENVIRONMENT=development
DEBUG=true
LOG_LEVEL=DEBUG
```

### Staging (.env.staging)
```bash
DATABASE_URL=postgresql+asyncpg://hexa_staging:StagingPass123@db-staging.internal:5432/hexa_staging
REDIS_URL=redis://redis-staging.internal:6379/0
REDIS_PASSWORD=StagingRedisPass123
RABBITMQ_URL=amqp://hexa_staging:StagingPass123@rabbitmq-staging.internal:5672/hexa_staging
JWT_SECRET_KEY=staging_jwt_secret_key_muy_larga_y_segura_aqui
ENVIRONMENT=staging
DEBUG=false
LOG_LEVEL=INFO
BACKEND_URL=https://api-staging.tu-dominio.com
FRONTEND_URL=https://staging.tu-dominio.com
```

### Producción (.env.production)
```bash
DATABASE_URL=postgresql+asyncpg://hexa_prod:ProductionSecurePass123@db-prod-cluster.internal:5432/hexa_prod
REDIS_URL=redis://redis-prod-cluster.internal:6379/0
REDIS_PASSWORD=ProductionRedisSecurePass123
RABBITMQ_URL=amqp://hexa_prod:ProductionRabbitPass123@rabbitmq-prod-cluster.internal:5672/hexa_prod
JWT_SECRET_KEY=production_jwt_super_secure_key_generated_with_secrets_module_length_64_chars
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=WARNING
BACKEND_URL=https://api.tu-dominio.com
FRONTEND_URL=https://tu-dominio.com

# Performance
DB_POOL_SIZE=50
DB_MAX_OVERFLOW=20

# Security
ALLOWED_HOSTS=["tu-dominio.com", "api.tu-dominio.com"]
CORS_ORIGINS=["https://tu-dominio.com"]
```

## Gestión Segura de Secretos

### ❌ NO Hacer
```bash
# NO commitear .env a git
git add .env  # ❌

# NO hardcodear secretos en código
JWT_SECRET_KEY = "mi-clave-secreta"  # ❌

# NO usar secretos débiles
JWT_SECRET_KEY=123456  # ❌
```

### ✅ Hacer

#### 1. Usar .env con .gitignore
```bash
# .gitignore
.env
.env.*
!.env.example
```

#### 2. Usar gestores de secretos

**AWS Secrets Manager**:
```python
import boto3
import json

def get_secret():
    client = boto3.client('secretsmanager', region_name='us-east-1')
    response = client.get_secret_value(SecretId='hexa-prod-secrets')
    return json.loads(response['SecretString'])

secrets = get_secret()
DATABASE_URL = secrets['DATABASE_URL']
```

**HashiCorp Vault**:
```python
import hvac

client = hvac.Client(url='https://vault.tu-dominio.com')
client.token = os.getenv('VAULT_TOKEN')

secret = client.secrets.kv.v2.read_secret_version(path='hexa/prod')
DATABASE_URL = secret['data']['data']['DATABASE_URL']
```

**Docker Secrets**:
```yaml
# docker-compose.prod.yaml
services:
  backend:
    secrets:
      - database_url
      - jwt_secret_key
    environment:
      DATABASE_URL_FILE: /run/secrets/database_url
      JWT_SECRET_KEY_FILE: /run/secrets/jwt_secret_key

secrets:
  database_url:
    external: true
  jwt_secret_key:
    external: true
```

#### 3. Variables de entorno del sistema
```bash
# En el servidor
export DATABASE_URL="postgresql+asyncpg://..."
export JWT_SECRET_KEY="..."

# O en systemd service
[Service]
Environment="DATABASE_URL=postgresql+asyncpg://..."
Environment="JWT_SECRET_KEY=..."
```

## Validación de Variables

### Script de Validación
```python
# scripts/validate_env.py
import sys
from core.config.settings import env

required_vars = [
    'DATABASE_URL',
    'REDIS_URL',
    'RABBITMQ_URL',
    'JWT_SECRET_KEY',
]

def validate_env():
    missing = []
    weak = []
    
    for var in required_vars:
        value = getattr(env, var, None)
        if not value:
            missing.append(var)
        elif var == 'JWT_SECRET_KEY' and len(value) < 32:
            weak.append(var)
    
    if missing:
        print(f"❌ Variables faltantes: {', '.join(missing)}")
        sys.exit(1)
    
    if weak:
        print(f"⚠️  Variables débiles: {', '.join(weak)}")
        sys.exit(1)
    
    print("✅ Todas las variables de entorno son válidas")

if __name__ == "__main__":
    validate_env()
```

**Ejecutar antes de deploy**:
```bash
docker compose -f compose.prod.yaml run --rm backend python scripts/validate_env.py
```

## Ejemplo .env.example

```bash
# .env.example - Template para configuración
# Copiar a .env y completar con valores reales

# Database
DATABASE_URL=postgresql+asyncpg://usuario:password@host:5432/database
DB_POOL_SIZE=20
DB_MAX_OVERFLOW=10

# Redis
REDIS_URL=redis://host:6379/0
REDIS_PASSWORD=tu_password

# RabbitMQ
RABBITMQ_URL=amqp://usuario:password@host:5672/vhost

# JWT
JWT_SECRET_KEY=cambiar_por_clave_segura_generada
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=30

# Paths
BACKEND_PATH=/api
FRONTEND_URL=https://tu-dominio.com
BACKEND_URL=https://api.tu-dominio.com

# AWS S3
AWS_ACCESS_KEY=tu_access_key
AWS_ACCESS_SECRET_KEY=tu_secret_key
AWS_ACCESS_REGION=us-east-1
AWS_ACCESS_BUCKET_NAME=tu-bucket

# Email
EMAIL_SMTP_SERVER=smtp.provider.com
EMAIL_SMTP_PORT=587
EMAIL_SMTP_USERNAME=usuario
EMAIL_SMTP_PASSWORD=password
EMAIL_SMTP_MAILSENDER=noreply@tu-dominio.com

# Environment
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=INFO
```

## Rotación de Secretos

### Proceso Recomendado

1. **Generar nuevo secreto**:
```bash
python -c "import secrets; print(secrets.token_urlsafe(64))"
```

2. **Actualizar en gestor de secretos**:
```bash
# AWS Secrets Manager
aws secretsmanager update-secret \
  --secret-id hexa-prod-jwt \
  --secret-string "nuevo_secreto"
```

3. **Rolling restart**:
```bash
# Reiniciar servicios uno por uno
docker compose -f compose.prod.yaml up -d --no-deps --scale backend=2 backend
docker compose -f compose.prod.yaml up -d --no-deps --scale backend=1 backend
```

4. **Verificar**:
```bash
docker compose -f compose.prod.yaml logs backend | grep "Application startup complete"
```

## Troubleshooting

### Error: "Connection refused" a Database
```bash
# Verificar conectividad
docker compose exec backend ping db-host

# Verificar credenciales
docker compose exec backend psql $DATABASE_URL -c "SELECT 1;"
```

### Error: JWT Token inválido
```bash
# Verificar JWT_SECRET_KEY
docker compose exec backend python -c "from core.config.settings import env; print(len(env.JWT_SECRET_KEY))"
# Debe ser > 32 caracteres
```

### Error: Redis connection failed
```bash
# Verificar Redis
docker compose exec backend redis-cli -h redis-host -a "$REDIS_PASSWORD" PING
```

## Checklist de Producción

- [ ] Todas las variables requeridas configuradas
- [ ] JWT_SECRET_KEY es segura (> 32 caracteres)
- [ ] Passwords no usan valores por defecto
- [ ] DATABASE_URL apunta a cluster de producción
- [ ] DEBUG=false
- [ ] LOG_LEVEL apropiado (INFO o WARNING)
- [ ] CORS_ORIGINS configurado correctamente
- [ ] Secretos en gestor de secretos (no en .env)
- [ ] .env NO está en git
- [ ] Backups de base de datos configurados
- [ ] Monitoreo de servicios activo

## Próximos Pasos

- [Docker Build](./02-docker-build.md) - Crear imágenes de producción
- [Monitoreo](./03-monitoring.md) - Logs y métricas
