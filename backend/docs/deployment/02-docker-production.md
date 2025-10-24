# Docker en Producción

## Dockerfiles

### Backend - Producción

```dockerfile
# docker/hexa/prod.Dockerfile
FROM python:3.11-slim as builder

# Instalar uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

# Copiar archivos de dependencias
COPY pyproject.toml uv.lock ./

# Instalar dependencias
RUN uv sync --frozen --no-dev

# Stage final
FROM python:3.11-slim

WORKDIR /app

# Copiar virtual env del builder
COPY --from=builder /app/.venv /app/.venv

# Copiar código fuente
COPY . .

# Variables de entorno
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Usuario no-root
RUN useradd -m -u 1000 hexa && \
    chown -R hexa:hexa /app
USER hexa

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
  CMD python -c "import requests; requests.get('http://localhost:8000/health')"

# Comando por defecto
CMD ["uvicorn", "core.fastapi.server:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Celery Worker - Producción

```dockerfile
# docker/hexa/celery-prod.Dockerfile
FROM python:3.11-slim as builder

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

FROM python:3.11-slim

WORKDIR /app

COPY --from=builder /app/.venv /app/.venv
COPY . .

ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

RUN useradd -m -u 1000 hexa && \
    chown -R hexa:hexa /app
USER hexa

CMD ["python", "-m", "hexa", "celery-apps"]
```

## Docker Compose - Producción

```yaml
# compose.prod.yaml
version: '3.8'

services:
  backend:
    build:
      context: .
      dockerfile: docker/hexa/prod.Dockerfile
    image: hexa-backend:${VERSION:-latest}
    restart: unless-stopped
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - REDIS_URL=${REDIS_URL}
      - REDIS_PASSWORD=${REDIS_PASSWORD}
      - RABBITMQ_URL=${RABBITMQ_URL}
      - JWT_SECRET_KEY=${JWT_SECRET_KEY}
      - ENVIRONMENT=production
      - LOG_LEVEL=INFO
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy
      rabbit:
        condition: service_healthy
    networks:
      - hexa-network
    deploy:
      replicas: 2
      resources:
        limits:
          cpus: '1'
          memory: 1G
        reservations:
          cpus: '0.5'
          memory: 512M

  celery_worker:
    build:
      context: .
      dockerfile: docker/hexa/celery-prod.Dockerfile
    image: hexa-celery:${VERSION:-latest}
    restart: unless-stopped
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - REDIS_URL=${REDIS_URL}
      - REDIS_PASSWORD=${REDIS_PASSWORD}
      - RABBITMQ_URL=${RABBITMQ_URL}
      - ENVIRONMENT=production
      - LOG_LEVEL=INFO
    depends_on:
      - rabbit
      - redis
    networks:
      - hexa-network
    deploy:
      replicas: 2
      resources:
        limits:
          cpus: '0.5'
          memory: 512M

  db:
    image: postgres:15-alpine
    restart: unless-stopped
    environment:
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
      POSTGRES_DB: ${DB_NAME}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${DB_USER}"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - hexa-network
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G

  redis:
    image: redis:7-alpine
    restart: unless-stopped
    command: redis-server --requirepass ${REDIS_PASSWORD}
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "-a", "${REDIS_PASSWORD}", "ping"]
      interval: 10s
      timeout: 3s
      retries: 5
    networks:
      - hexa-network

  rabbit:
    image: rabbitmq:4-management-alpine
    restart: unless-stopped
    environment:
      RABBITMQ_DEFAULT_USER: ${RABBIT_USER}
      RABBITMQ_DEFAULT_PASS: ${RABBIT_PASSWORD}
    volumes:
      - rabbitmq_data:/var/lib/rabbitmq
    healthcheck:
      test: ["CMD", "rabbitmq-diagnostics", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - hexa-network

  nginx:
    image: nginx:alpine
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./docker/nginx/nginx.prod.conf:/etc/nginx/nginx.conf:ro
      - ./docker/nginx/ssl:/etc/nginx/ssl:ro
      - nginx_logs:/var/log/nginx
    depends_on:
      - backend
    networks:
      - hexa-network

volumes:
  postgres_data:
  redis_data:
  rabbitmq_data:
  nginx_logs:

networks:
  hexa-network:
    driver: bridge
```

## Nginx Configuration

```nginx
# docker/nginx/nginx.prod.conf
upstream backend {
    least_conn;
    server backend:8000 max_fails=3 fail_timeout=30s;
}

# Redirect HTTP to HTTPS
server {
    listen 80;
    server_name api.tu-dominio.com;
    return 301 https://$server_name$request_uri;
}

# HTTPS Server
server {
    listen 443 ssl http2;
    server_name api.tu-dominio.com;

    # SSL Configuration
    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    # Security Headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # Compression
    gzip on;
    gzip_vary on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml;

    # Logging
    access_log /var/log/nginx/access.log combined;
    error_log /var/log/nginx/error.log warn;

    # Rate Limiting
    limit_req_zone $binary_remote_addr zone=api_limit:10m rate=10r/s;
    limit_req zone=api_limit burst=20 nodelay;

    location /api/ {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
        
        # WebSocket support
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }

    location /health {
        proxy_pass http://backend/health;
        access_log off;
    }
}
```

## Build y Push

### Script de Build

```bash
#!/bin/bash
# scripts/build.sh

VERSION=${1:-latest}
REGISTRY="registry.tu-dominio.com"

echo "🔨 Building images version: $VERSION"

# Build backend
docker build \
  -t ${REGISTRY}/hexa-backend:${VERSION} \
  -t ${REGISTRY}/hexa-backend:latest \
  -f docker/hexa/prod.Dockerfile \
  .

# Build celery
docker build \
  -t ${REGISTRY}/hexa-celery:${VERSION} \
  -t ${REGISTRY}/hexa-celery:latest \
  -f docker/hexa/celery-prod.Dockerfile \
  .

echo "✅ Images built successfully"

# Push
if [ "$2" == "push" ]; then
    echo "📤 Pushing images..."
    docker push ${REGISTRY}/hexa-backend:${VERSION}
    docker push ${REGISTRY}/hexa-backend:latest
    docker push ${REGISTRY}/hexa-celery:${VERSION}
    docker push ${REGISTRY}/hexa-celery:latest
    echo "✅ Images pushed successfully"
fi
```

**Uso**:
```bash
# Build local
./scripts/build.sh v1.0.0

# Build y push
./scripts/build.sh v1.0.0 push
```

### GitHub Actions CI/CD

```yaml
# .github/workflows/deploy.yml
name: Build and Deploy

on:
  push:
    tags:
      - 'v*'

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  build:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Log in to Container Registry
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}

      - name: Build and push Backend
        uses: docker/build-push-action@v5
        with:
          context: ./backend
          file: ./backend/docker/hexa/prod.Dockerfile
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}

      - name: Build and push Celery
        uses: docker/build-push-action@v5
        with:
          context: ./backend
          file: ./backend/docker/hexa/celery-prod.Dockerfile
          push: true
          tags: ${{ steps.meta.outputs.tags }}-celery
          labels: ${{ steps.meta.outputs.labels }}

  deploy:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to production
        uses: appleboy/ssh-action@master
        with:
          host: ${{ secrets.PROD_HOST }}
          username: ${{ secrets.PROD_USER }}
          key: ${{ secrets.PROD_SSH_KEY }}
          script: |
            cd /opt/hexa
            docker compose -f compose.prod.yaml pull
            docker compose -f compose.prod.yaml up -d --no-deps backend celery_worker
            docker compose -f compose.prod.yaml exec backend alembic upgrade head
```

## Deploy a Producción

### Primera vez

```bash
# 1. SSH al servidor
ssh user@production-server

# 2. Crear directorio
mkdir -p /opt/hexa
cd /opt/hexa

# 3. Copiar archivos
scp compose.prod.yaml .env user@production-server:/opt/hexa/
scp -r docker/ user@production-server:/opt/hexa/

# 4. Pull images
docker compose -f compose.prod.yaml pull

# 5. Iniciar servicios
docker compose -f compose.prod.yaml up -d

# 6. Ejecutar migraciones
docker compose -f compose.prod.yaml exec backend alembic upgrade head

# 7. Verificar
docker compose -f compose.prod.yaml ps
docker compose -f compose.prod.yaml logs backend
```

### Updates

```bash
# 1. Pull nuevas images
docker compose -f compose.prod.yaml pull

# 2. Rolling update (zero downtime)
docker compose -f compose.prod.yaml up -d --no-deps --scale backend=3 backend
sleep 10
docker compose -f compose.prod.yaml up -d --no-deps --scale backend=2 backend

# 3. Migrar base de datos
docker compose -f compose.prod.yaml exec backend alembic upgrade head

# 4. Reiniciar celery
docker compose -f compose.prod.yaml restart celery_worker

# 5. Verificar
curl https://api.tu-dominio.com/health
```

## Rollback

```bash
# 1. Tag anterior
VERSION_ANTERIOR=v1.0.0

# 2. Pull versión anterior
docker pull registry.tu-dominio.com/hexa-backend:$VERSION_ANTERIOR
docker pull registry.tu-dominio.com/hexa-celery:$VERSION_ANTERIOR

# 3. Tag como latest
docker tag registry.tu-dominio.com/hexa-backend:$VERSION_ANTERIOR hexa-backend:latest
docker tag registry.tu-dominio.com/hexa-celery:$VERSION_ANTERIOR hexa-celery:latest

# 4. Deploy
docker compose -f compose.prod.yaml up -d

# 5. Rollback migraciones (si necesario)
docker compose -f compose.prod.yaml exec backend alembic downgrade -1
```

## Monitoreo

Ver [Monitoreo](./03-monitoring.md) para configuración completa de logs y métricas.

## Checklist de Producción

- [ ] Dockerfile multi-stage para reducir tamaño
- [ ] Usuario no-root en containers
- [ ] Health checks configurados
- [ ] Resource limits definidos
- [ ] SSL/TLS configurado en Nginx
- [ ] Rate limiting activo
- [ ] Logs centralizados
- [ ] Backup de volúmenes
- [ ] Secrets gestionados correctamente
- [ ] CI/CD pipeline funcionando
- [ ] Rollback plan documentado
- [ ] Monitoreo activo

## Próximos Pasos

- [Monitoreo](./03-monitoring.md) - Logs y métricas
- [Environment Variables](./01-environment.md) - Configuración
