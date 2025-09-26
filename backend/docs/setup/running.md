# Ejecución del Sistema

## Inicio Rápido

### 1. Desarrollo Local (Recomendado)
```bash
# Ejecutar con el comando hexa
uv run hexa api --dev

# O usando el alias corto
uv run hexa dev
```

### 2. Alternativas de Ejecución
```bash
# Usando uvicorn directamente
uv run uvicorn core.fastapi.server:app --reload --host 0.0.0.0 --port 8000

# Usando main.py (versión mínima)
uv run python main.py
```

### 3. Verificar Funcionamiento
```bash
# Health check
curl http://localhost:8000/health

# Documentación API
open http://localhost:8000/docs

# Listar módulos activos
curl http://localhost:8000/modules

# Verificar permisos del sistema
curl http://localhost:8000/permissions
```

## Modos de Ejecución

### Desarrollo
```bash
# Ejecutar en modo desarrollo (recomendado)
uv run hexa api --dev

# Con configuración manual
export DEBUG=true
export LOG_LEVEL=DEBUG
export RELOAD=true
uv run python main.py
```

**Características**:
- Recarga automática de código
- Logging detallado
- CORS permisivo
- Base de datos SQLite local
- Auto-registro de módulos
- Service Locator activo
- Sistema de permisos habilitado

### Testing
```bash
# Configuración de testing
export ENVIRONMENT=testing
export DATABASE_URL=sqlite:///:memory:

# Ejecutar tests
uv run pytest

# Con cobertura
uv run pytest --cov=modules tests/

# Test específico de módulos
uv run pytest tests/modules/
```

### Staging
```bash
# Configuración de staging
export ENVIRONMENT=staging
export DEBUG=false
export LOG_LEVEL=INFO

# Ejecutar con Gunicorn
gunicorn main:app -w 2 -k uvicorn.workers.UvicornWorker
```

### Producción
```bash
# Configuración de producción
export ENVIRONMENT=production
export DEBUG=false
export LOG_LEVEL=WARNING

# Ejecutar con múltiples workers
gunicorn core.fastapi.server:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## Configuración de Servidor

### Uvicorn (Desarrollo)
```bash
# Básico
uvicorn main:app

# Con opciones
uvicorn main:app \
  --host 0.0.0.0 \
  --port 8000 \
  --reload \
  --log-level debug
```

### Gunicorn (Producción)
```bash
# Configuración básica
gunicorn main:app -k uvicorn.workers.UvicornWorker

# Configuración completa
gunicorn main:app \
  -k uvicorn.workers.UvicornWorker \
  -w 4 \
  --bind 0.0.0.0:8000 \
  --access-logfile - \
  --error-logfile - \
  --log-level info
```

### Configuración con Archivo
```python
# gunicorn.conf.py
bind = "0.0.0.0:8000"
workers = 4
worker_class = "uvicorn.workers.UvicornWorker"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 100
timeout = 30
keepalive = 2
preload_app = True
```

```bash
# Ejecutar con archivo de configuración
gunicorn main:app -c gunicorn.conf.py
```

## Docker

### Desarrollo con Docker
```bash
# Construir imagen
docker build -t fast-hexagonal .

# Ejecutar contenedor
docker run -p 8000:8000 --env-file .env.development fast-hexagonal
```

### Docker Compose
```bash
# Levantar todos los servicios
docker-compose up -d

# Ver logs
docker-compose logs -f app

# Parar servicios
docker-compose down
```

### Docker Compose Override
```yaml
# docker-compose.override.yml (desarrollo)
version: '3.8'

services:
  app:
    volumes:
      - .:/app
    environment:
      - DEBUG=true
      - RELOAD=true
    command: uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## Scripts de Ejecución

### Makefile
```makefile
.PHONY: run run-dev run-prod test

run:
	python main.py

run-dev:
	DEBUG=true RELOAD=true python main.py

run-prod:
	gunicorn main:app -c gunicorn.conf.py

test:
	pytest

docker-build:
	docker build -t fast-hexagonal .

docker-run:
	docker run -p 8000:8000 --env-file .env fast-hexagonal
```

### Scripts Shell
```bash
#!/bin/bash
# scripts/run-dev.sh
export DEBUG=true
export RELOAD=true
export LOG_LEVEL=DEBUG

echo "Starting development server..."
python main.py
```

```bash
#!/bin/bash
# scripts/run-prod.sh
export ENVIRONMENT=production
export DEBUG=false
export LOG_LEVEL=INFO

echo "Starting production server..."
gunicorn main:app -c gunicorn.conf.py
```

## Monitoreo y Logs

### Logging en Tiempo Real
```bash
# Seguir logs de aplicación
tail -f logs/app.log

# Filtrar por nivel
tail -f logs/app.log | grep ERROR

# Logs de módulo específico
tail -f logs/app.log | grep "modules.user"
```

### Métricas del Sistema
```bash
# Endpoint de métricas
curl http://localhost:8000/metrics

# Health check detallado
curl http://localhost:8000/health | jq
```

### Monitoreo de Procesos
```bash
# Ver procesos Python
ps aux | grep python

# Monitorear recursos
htop

# Conexiones de red
netstat -tulpn | grep :8000
```

## Gestión de Procesos

### Systemd (Linux)
```ini
# /etc/systemd/system/fast-hexagonal.service
[Unit]
Description=Fast Hexagonal API
After=network.target

[Service]
Type=exec
User=www-data
Group=www-data
WorkingDirectory=/opt/fast-hexagonal
Environment=PATH=/opt/fast-hexagonal/.venv/bin
EnvironmentFile=/opt/fast-hexagonal/.env.production
ExecStart=/opt/fast-hexagonal/.venv/bin/gunicorn main:app -c gunicorn.conf.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
# Gestionar servicio
sudo systemctl enable fast-hexagonal
sudo systemctl start fast-hexagonal
sudo systemctl status fast-hexagonal
```

### Supervisor
```ini
# /etc/supervisor/conf.d/fast-hexagonal.conf
[program:fast-hexagonal]
command=/opt/fast-hexagonal/.venv/bin/gunicorn main:app -c gunicorn.conf.py
directory=/opt/fast-hexagonal
user=www-data
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/fast-hexagonal.log
```

```bash
# Gestionar con supervisor
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start fast-hexagonal
```

## Proxy Reverso

### Nginx
```nginx
# /etc/nginx/sites-available/fast-hexagonal
server {
    listen 80;
    server_name api.yourapp.com;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # WebSocket support
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
    
    # Static files (if any)
    location /static/ {
        alias /opt/fast-hexagonal/static/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

### Apache
```apache
# /etc/apache2/sites-available/fast-hexagonal.conf
<VirtualHost *:80>
    ServerName api.yourapp.com
    
    ProxyPreserveHost On
    ProxyRequests Off
    ProxyPass / http://127.0.0.1:8000/
    ProxyPassReverse / http://127.0.0.1:8000/
    
    # Headers
    ProxyPassReverse / http://127.0.0.1:8000/
    ProxyPreserveHost On
    ProxyAddHeaders On
</VirtualHost>
```

## Troubleshooting

### Puerto en Uso
```bash
# Encontrar proceso usando puerto 8000
lsof -i :8000

# Matar proceso
kill -9 <PID>

# Usar puerto diferente
uvicorn main:app --port 8001
```

### Problemas de Permisos
```bash
# Verificar permisos
ls -la main.py

# Dar permisos de ejecución
chmod +x main.py

# Cambiar propietario
sudo chown $USER:$USER -R .
```

### Problemas de Dependencias
```bash
# Reinstalar dependencias
pip install --force-reinstall -r requirements.txt

# Verificar instalación
pip list | grep fastapi

# Limpiar cache
pip cache purge
```

### Problemas de Base de Datos
```bash
# Verificar conexión
python -c "from core.db.session import engine; print(engine.url)"

# Ejecutar migraciones
alembic upgrade head

# Verificar tablas
python -c "from core.db.session import engine; print(engine.table_names())"
```

### Logs de Error
```bash
# Ver últimos errores
tail -n 50 logs/app.log | grep ERROR

# Logs de inicio
journalctl -u fast-hexagonal -f

# Logs de Docker
docker-compose logs -f app
```

## Comandos Útiles

### Desarrollo
```bash
# Reinicio rápido
pkill -f "python main.py" && python main.py

# Limpiar cache Python
find . -name "*.pyc" -delete
find . -name "__pycache__" -type d -exec rm -rf {} +

# Verificar sintaxis
python -m py_compile main.py
```

### Producción
```bash
# Reinicio graceful
sudo systemctl reload fast-hexagonal

# Ver estado del servicio
sudo systemctl status fast-hexagonal

# Ver logs del sistema
journalctl -u fast-hexagonal --since "1 hour ago"
```