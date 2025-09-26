# Troubleshooting

## Problemas Comunes y Soluciones

### Problemas de Instalación

#### Error: "Module not found"
```bash
ModuleNotFoundError: No module named 'modules.auth'
```

**Solución:**
```bash
# Verificar PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# O instalar en modo desarrollo
pip install -e .

# Verificar estructura de directorios
ls -la modules/
```

#### Error: "Permission denied"
```bash
PermissionError: [Errno 13] Permission denied: '/path/to/file'
```

**Solución:**
```bash
# Dar permisos apropiados
chmod +x main.py
chmod -R 755 modules/

# Verificar propietario
sudo chown -R $USER:$USER .
```

### Problemas de Base de Datos

#### Error: "Database connection failed"
```bash
sqlalchemy.exc.OperationalError: (psycopg2.OperationalError) could not connect to server
```

**Diagnóstico:**
```bash
# Verificar conexión a PostgreSQL
psql -h localhost -U postgres -d fast_hexagonal

# Verificar variables de entorno
echo $DATABASE_URL

# Verificar servicio
sudo systemctl status postgresql
```

**Solución:**
```bash
# Iniciar PostgreSQL
sudo systemctl start postgresql

# Crear base de datos si no existe
sudo -u postgres createdb fast_hexagonal

# Verificar configuración en .env
DATABASE_URL=postgresql://postgres:password@localhost:5432/fast_hexagonal
```

#### Error: "Table doesn't exist"
```bash
sqlalchemy.exc.ProgrammingError: (psycopg2.errors.UndefinedTable) relation "users" does not exist
```

**Solución:**
```bash
# Ejecutar migraciones
alembic upgrade head

# Verificar estado de migraciones
alembic current

# Ver historial de migraciones
alembic history
```

#### Error: "Migration conflict"
```bash
alembic.util.exc.CommandError: Multiple head revisions are present
```

**Solución:**
```bash
# Ver heads múltiples
alembic heads

# Mergear heads
alembic merge -m "merge heads" head1 head2

# Aplicar merge
alembic upgrade head
```

### Problemas de Redis

#### Error: "Redis connection refused"
```bash
redis.exceptions.ConnectionError: Error 111 connecting to localhost:6379. Connection refused.
```

**Diagnóstico:**
```bash
# Verificar servicio Redis
redis-cli ping

# Verificar proceso
ps aux | grep redis

# Verificar puerto
netstat -tulpn | grep :6379
```

**Solución:**
```bash
# Iniciar Redis
sudo systemctl start redis-server

# O con Docker
docker run -d -p 6379:6379 redis:alpine

# Verificar configuración
echo $REDIS_URL
```

### Problemas de Autenticación

#### Error: "Invalid token"
```bash
HTTPException: 401 Unauthorized - Could not validate credentials
```

**Diagnóstico:**
```bash
# Verificar token
curl -H "Authorization: Bearer $TOKEN" http://localhost:8000/auth/verify

# Decodificar JWT (sin verificar)
python -c "
import jwt
token = 'your-token-here'
print(jwt.decode(token, options={'verify_signature': False}))
"
```

**Solución:**
```bash
# Obtener nuevo token
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password"}'

# Verificar configuración JWT
echo $JWT_SECRET_KEY
echo $JWT_ALGORITHM
```

#### Error: "Token expired"
```bash
HTTPException: 401 Unauthorized - Token has expired
```

**Solución:**
```bash
# Usar refresh token
curl -X POST http://localhost:8000/auth/refresh \
  -H "Content-Type: application/json" \
  -d '{"refresh_token": "your-refresh-token"}'

# Verificar configuración de expiración
echo $JWT_ACCESS_TOKEN_EXPIRE_MINUTES
```

### Problemas de Permisos RBAC

#### Error: "Permission required"
```bash
HTTPException: 403 Forbidden - Permission required: user:create
```

**Diagnóstico:**
```bash
# Verificar permisos del usuario
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:8000/rbac/users/1/roles

# Verificar permisos del rol
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:8000/rbac/roles/1/permissions
```

**Solución:**
```bash
# Asignar rol al usuario
curl -X POST -H "Authorization: Bearer $ADMIN_TOKEN" \
  http://localhost:8000/rbac/users/1/roles/2

# Asignar permiso al rol
curl -X POST -H "Authorization: Bearer $ADMIN_TOKEN" \
  http://localhost:8000/rbac/roles/2/permissions/1
```

### Problemas de Módulos

#### Error: "Module not registered"
```bash
WARNING - Module user_service not found in service locator
```

**Diagnóstico:**
```bash
# Verificar módulos registrados
curl http://localhost:8000/health

# Verificar logs de inicialización
tail -f logs/app.log | grep "Module"
```

**Solución:**
```bash
# Verificar que el módulo está habilitado
echo $USER_MODULE_ENABLED

# Verificar estructura del módulo
ls -la modules/user/

# Verificar implementación de ModuleInterface
python -c "
from modules.user.module import UserModule
module = UserModule()
print(f'Name: {module.name}')
print(f'Enabled: {module.enabled}')
"
```

#### Error: "Circular dependency"
```bash
ValueError: Circular dependency detected involving module_a
```

**Solución:**
```bash
# Revisar dependencias en module.py
grep -r "dependencies" modules/*/module.py

# Rediseñar dependencias para evitar ciclos
# Usar eventos en lugar de dependencias directas
```

### Problemas de Performance

#### Error: "Request timeout"
```bash
TimeoutError: Request timed out after 30 seconds
```

**Diagnóstico:**
```bash
# Verificar conexiones de base de datos
python -c "
from core.db.session import engine
print(f'Pool size: {engine.pool.size()}')
print(f'Checked out: {engine.pool.checkedout()}')
"

# Verificar queries lentas
tail -f logs/app.log | grep "slow query"
```

**Solución:**
```bash
# Aumentar pool de conexiones
DB_POOL_SIZE=20
DB_MAX_OVERFLOW=30

# Optimizar queries
# Agregar índices en base de datos
# Implementar caché
```

#### Error: "Memory usage high"
```bash
# Verificar uso de memoria
ps aux | grep python
htop

# Verificar memory leaks
python -m memory_profiler main.py
```

**Solución:**
```bash
# Configurar límites de memoria
ulimit -v 1000000  # 1GB

# Optimizar código
# Usar generadores en lugar de listas
# Limpiar referencias no utilizadas
```

### Problemas de Networking

#### Error: "Connection refused"
```bash
requests.exceptions.ConnectionError: HTTPConnectionPool(host='localhost', port=8000): Max retries exceeded
```

**Diagnóstico:**
```bash
# Verificar que el servidor está corriendo
ps aux | grep python

# Verificar puerto
netstat -tulpn | grep :8000

# Verificar firewall
sudo ufw status
```

**Solución:**
```bash
# Iniciar servidor
python main.py

# Verificar configuración de host
HOST=0.0.0.0
PORT=8000

# Verificar logs de inicio
tail -f logs/app.log
```

### Problemas de Docker

#### Error: "Container won't start"
```bash
docker: Error response from daemon: Container command not found
```

**Diagnóstico:**
```bash
# Verificar Dockerfile
cat Dockerfile

# Verificar imagen
docker images

# Verificar logs del container
docker logs container_name
```

**Solución:**
```bash
# Reconstruir imagen
docker build -t fast-hexagonal .

# Verificar comando de entrada
docker run -it fast-hexagonal /bin/bash

# Verificar variables de entorno
docker run --env-file .env fast-hexagonal
```

#### Error: "Volume mount failed"
```bash
docker: Error response from daemon: invalid mount config
```

**Solución:**
```bash
# Verificar rutas absolutas
docker run -v $(pwd):/app fast-hexagonal

# Verificar permisos
chmod -R 755 .

# Usar bind mounts correctamente
docker run -v /host/path:/container/path fast-hexagonal
```

## Herramientas de Diagnóstico

### Health Check Script
```python
# scripts/health_check.py
import requests
import sys

def check_health():
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Status: {data['status']}")
            print(f"✅ Modules: {len(data['modules'])}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

if __name__ == "__main__":
    if not check_health():
        sys.exit(1)
```

### Database Check Script
```python
# scripts/db_check.py
from core.db.session import engine
from sqlalchemy import text

def check_database():
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("✅ Database connection OK")
            
            # Verificar tablas principales
            tables = ['users', 'roles', 'permissions']
            for table in tables:
                result = conn.execute(text(f"SELECT COUNT(*) FROM {table}"))
                count = result.scalar()
                print(f"✅ Table {table}: {count} records")
            
            return True
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False

if __name__ == "__main__":
    check_database()
```

### Module Check Script
```python
# scripts/module_check.py
from shared.interfaces.module_registry import module_registry

def check_modules():
    modules = module_registry.get_all_modules()
    
    print(f"📦 Total modules: {len(modules)}")
    
    for name, module in modules.items():
        print(f"  ✅ {name} v{module.version}")
        print(f"     Dependencies: {module.dependencies}")
        print(f"     Enabled: {module.enabled}")
        
        # Verificar container
        try:
            container = module.container
            print(f"     Container: OK")
        except Exception as e:
            print(f"     Container: ❌ {e}")
        
        # Verificar rutas
        try:
            routes = module.routes
            print(f"     Routes: OK")
        except Exception as e:
            print(f"     Routes: ❌ {e}")
        
        print()

if __name__ == "__main__":
    check_modules()
```

## Logs y Monitoreo

### Configurar Logging Detallado
```python
# config/logging.py
import logging.config

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "detailed": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(module)s:%(lineno)d - %(message)s"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "detailed",
            "level": "DEBUG"
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "logs/debug.log",
            "maxBytes": 10485760,  # 10MB
            "backupCount": 5,
            "formatter": "detailed",
            "level": "DEBUG"
        }
    },
    "loggers": {
        "modules": {
            "handlers": ["console", "file"],
            "level": "DEBUG",
            "propagate": False
        }
    }
}

logging.config.dictConfig(LOGGING_CONFIG)
```

### Comandos de Monitoreo
```bash
# Ver logs en tiempo real
tail -f logs/app.log

# Filtrar errores
tail -f logs/app.log | grep ERROR

# Ver logs de módulo específico
tail -f logs/app.log | grep "modules.user"

# Monitorear performance
htop
iotop
nethogs

# Verificar conexiones de red
ss -tulpn | grep :8000
```

## Contacto y Soporte

### Información de Debug
Cuando reportes un problema, incluye:

1. **Versión del sistema**
2. **Logs relevantes**
3. **Configuración de entorno**
4. **Pasos para reproducir**
5. **Comportamiento esperado vs actual**

### Script de Información del Sistema
```bash
#!/bin/bash
# scripts/system_info.sh

echo "=== System Information ==="
echo "OS: $(uname -a)"
echo "Python: $(python --version)"
echo "Pip packages:"
pip list | grep -E "(fastapi|sqlalchemy|redis|alembic)"

echo -e "\n=== Environment Variables ==="
env | grep -E "(DATABASE_URL|REDIS_URL|JWT_|DEBUG)" | sed 's/=.*/=***/'

echo -e "\n=== Service Status ==="
systemctl is-active postgresql || echo "PostgreSQL: not running"
systemctl is-active redis || echo "Redis: not running"

echo -e "\n=== Application Health ==="
curl -s http://localhost:8000/health | jq . || echo "Application not responding"

echo -e "\n=== Recent Errors ==="
tail -n 20 logs/app.log | grep ERROR || echo "No recent errors"
```

### Generar Reporte de Debug
```bash
# Ejecutar script de información
./scripts/system_info.sh > debug_report.txt

# Agregar logs recientes
echo -e "\n=== Recent Logs ===" >> debug_report.txt
tail -n 100 logs/app.log >> debug_report.txt

# Comprimir para envío
tar -czf debug_report.tar.gz debug_report.txt logs/
```