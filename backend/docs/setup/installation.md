# Instalación

## Requisitos del Sistema

### Software Requerido
- **Python**: 3.11 o superior
- **PostgreSQL**: 13 o superior (opcional, SQLite por defecto)
- **Redis**: 6 o superior
- **Git**: Para clonar el repositorio

### Herramientas Recomendadas
- **uv**: Gestor de paquetes Python rápido
- **Docker**: Para servicios auxiliares
- **Make**: Para comandos automatizados

## Instalación Rápida

### 1. Clonar Repositorio
```bash
git clone <repository-url>
cd fast-hexagonal/backend
```

### 2. Configurar Entorno Virtual
```bash
# Con uv (recomendado)
uv venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows

# Con pip tradicional
python -m venv .venv
source .venv/bin/activate
```

### 3. Instalar Dependencias
```bash
# Con uv
uv pip install -r requirements.txt

# Con pip
pip install -r requirements.txt
```

### 4. Configurar Variables de Entorno
```bash
cp .env.example .env
# Editar .env con tus configuraciones
```

### 5. Inicializar Base de Datos
```bash
# Ejecutar migraciones
alembic upgrade head

# Crear datos iniciales (opcional)
python scripts/seed_data.py
```

### 6. Ejecutar Aplicación
```bash
python main.py
```

## Instalación Detallada

### Configuración con Docker

#### 1. Servicios Auxiliares
```bash
# Levantar Redis y PostgreSQL
docker-compose up -d redis postgres
```

#### 2. Configuración de Base de Datos
```bash
# Crear base de datos
docker exec -it postgres psql -U postgres -c "CREATE DATABASE fast_hexagonal;"

# Configurar .env
DATABASE_URL=postgresql://postgres:password@localhost:5432/fast_hexagonal
REDIS_URL=redis://localhost:6379/0
```

### Configuración Manual

#### 1. PostgreSQL
```bash
# Ubuntu/Debian
sudo apt-get install postgresql postgresql-contrib

# macOS
brew install postgresql

# Crear base de datos
sudo -u postgres createdb fast_hexagonal
sudo -u postgres createuser --interactive
```

#### 2. Redis
```bash
# Ubuntu/Debian
sudo apt-get install redis-server

# macOS
brew install redis

# Iniciar servicio
redis-server
```

## Verificación de Instalación

### 1. Health Check
```bash
curl http://localhost:8000/health
```

Respuesta esperada:
```json
{
    "status": "healthy",
    "modules": ["auth", "user", "rbac", "finance", "provider", "yiqi_erp"],
    "architecture": "hexagonal_decoupled"
}
```

### 2. Documentación API
Visitar: `http://localhost:8000/docs`

### 3. Tests
```bash
# Ejecutar tests unitarios
pytest tests/unit/

# Ejecutar tests de integración
pytest tests/integration/

# Cobertura
pytest --cov=modules tests/
```

## Configuración de Desarrollo

### 1. Pre-commit Hooks
```bash
pip install pre-commit
pre-commit install
```

### 2. Herramientas de Desarrollo
```bash
# Linting
ruff check .
ruff format .

# Type checking
pyright

# Security scanning
bandit -r modules/
```

### 3. Variables de Desarrollo
```bash
# .env.development
DEBUG=true
LOG_LEVEL=DEBUG
RELOAD=true
```

## Configuración de Producción

### 1. Variables de Producción
```bash
# .env.production
DEBUG=false
LOG_LEVEL=INFO
DATABASE_URL=postgresql://user:pass@prod-db:5432/db
REDIS_URL=redis://prod-redis:6379/0
SECRET_KEY=your-super-secret-key
```

### 2. Servidor WSGI
```bash
# Con Gunicorn
pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker

# Con Uvicorn
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### 3. Proxy Reverso (Nginx)
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## Solución de Problemas

### Error: Módulo no encontrado
```bash
# Verificar PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# O instalar en modo desarrollo
pip install -e .
```

### Error: Base de datos no conecta
```bash
# Verificar conexión
psql -h localhost -U postgres -d fast_hexagonal

# Verificar variables de entorno
echo $DATABASE_URL
```

### Error: Redis no disponible
```bash
# Verificar servicio
redis-cli ping

# Verificar configuración
echo $REDIS_URL
```

### Error: Permisos de archivo
```bash
# Dar permisos de ejecución
chmod +x scripts/*.py

# Verificar propietario
chown -R $USER:$USER .
```

## Comandos Útiles

### Makefile
```makefile
.PHONY: install run test clean

install:
	uv pip install -r requirements.txt

run:
	python main.py

test:
	pytest

clean:
	find . -type d -name __pycache__ -delete
	find . -name "*.pyc" -delete

migrate:
	alembic upgrade head

seed:
	python scripts/seed_data.py
```

### Scripts de Utilidad
```bash
# Ejecutar con make
make install
make run
make test

# O directamente
./scripts/setup.sh
./scripts/run-dev.sh
./scripts/run-tests.sh
```