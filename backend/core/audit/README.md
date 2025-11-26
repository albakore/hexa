# Sistema de Auditoría Automática

Sistema completo de auditoría que registra automáticamente todos los cambios (INSERT, UPDATE, DELETE) realizados en las entidades de la aplicación.

## Características

✅ **Auditoría Automática**: Registra cambios sin código adicional
✅ **Historial Completo**: Guarda valores antes y después de cada cambio
✅ **Trazabilidad**: Registra quién, cuándo y desde dónde se hizo el cambio
✅ **Contexto Rico**: Captura IP, user agent, endpoint, metadatos
✅ **No Intrusivo**: Solo requiere agregar un mixin a los modelos
✅ **Consultas Flexibles**: API para consultar el historial de cambios

## Arquitectura

### Componentes

1. **AuditLog**: Modelo que almacena los registros de auditoría
2. **AuditMixin**: Mixin para marcar modelos como auditables
3. **Context**: Sistema para capturar el usuario y contexto actual
4. **Listeners**: Event listeners que capturan cambios automáticamente
5. **Middleware**: Configura el contexto en cada request HTTP

### Flujo de Auditoría

```
Request → Middleware → Set Context → DB Operation → Event Listener → AuditLog → Response
                                           ↓
                                    Update created_by
                                    Update updated_by
```

## Instalación y Configuración

### 1. Configurar el Middleware

En tu archivo principal de FastAPI:

```python
from fastapi import FastAPI
from core.audit.middleware import AuditMiddleware
from core.audit import setup_audit_listeners

app = FastAPI()

# Configurar listeners de auditoría (una vez al inicio)
setup_audit_listeners()

# Agregar middleware
app.add_middleware(AuditMiddleware)
```

### 2. Agregar Dependencia de Usuario

Para que el sistema capture el usuario autenticado:

```python
from fastapi import Depends, Request
from core.auth import get_current_user  # Tu función de autenticación

@app.get("/protected")
async def protected_route(
	request: Request,
	user = Depends(get_current_user)
):
	# Establecer usuario en el request state
	request.state.user = user

	# Tu lógica aquí...
```

### 3. Marcar Modelos como Auditables

Agrega `AuditMixin` a los modelos que quieres auditar:

```python
from sqlmodel import SQLModel, Field
from shared.mixins import AuditMixin, TimestampMixin

class Provider(AuditMixin, TimestampMixin, SQLModel, table=True):
	id: int | None = Field(None, primary_key=True)
	name: str
	currency: str | None = None

	# created_at, updated_at, created_by, updated_by
	# se agregan automáticamente
```

## Uso

### Cambios Se Registran Automáticamente

```python
# CREATE - Se registra INSERT
provider = Provider(name="ABC Corp", currency="USD")
await repository.save(provider)
# AuditLog: action=INSERT, new_values={name, currency}, created_by=user_id

# UPDATE - Se registra UPDATE
provider.name = "XYZ Corp"
await repository.save(provider)
# AuditLog: action=UPDATE, old_values={name: "ABC"}, new_values={name: "XYZ"}
#           changed_fields=["name"], updated_by=user_id

# DELETE - Se registra DELETE
await repository.delete(provider)
# AuditLog: action=DELETE, old_values={all fields}
```

### Modelo AuditLog

Campos registrados en cada cambio:

```python
class AuditLog:
	id: int                          # ID incremental (BIGSERIAL en PostgreSQL)
	entity_name: str                 # Nombre del modelo (ej: "Provider")
	entity_id: str                   # ID del registro modificado
	action: str                      # "INSERT", "UPDATE", "DELETE"

	# Usuario
	user_id: uuid.UUID               # ID del usuario que hizo el cambio
	user_email: str                  # Email del usuario

	# Timestamp
	timestamp: datetime              # Cuándo se hizo el cambio

	# Datos del cambio
	old_values: dict                 # Valores anteriores (JSONB en PostgreSQL)
	new_values: dict                 # Valores nuevos (JSONB en PostgreSQL)
	changed_fields: list             # Lista de campos que cambiaron

	# Contexto
	ip_address: str                  # IP del cliente
	user_agent: str                  # Navegador/cliente
	endpoint: str                    # Endpoint de la API
	extra_data: dict                 # Datos adicionales personalizados (JSONB)
```

### Consultar Auditoría

#### Por Entidad

```python
from core.audit.models import AuditLog
from sqlmodel import select

# Obtener historial de un proveedor
query = select(AuditLog).where(
	AuditLog.entity_name == "Provider",
	AuditLog.entity_id == "123"
).order_by(AuditLog.timestamp.desc())

logs = await session.execute(query)
```

#### Por Usuario

```python
# Obtener cambios realizados por un usuario
query = select(AuditLog).where(
	AuditLog.user_id == user.id
).order_by(AuditLog.timestamp.desc())
```

#### Por Fecha

```python
from datetime import datetime, timedelta

# Cambios de las últimas 24 horas
yesterday = datetime.now() - timedelta(days=1)
query = select(AuditLog).where(
	AuditLog.timestamp >= yesterday
)
```

#### Por Acción

```python
# Solo eliminaciones
query = select(AuditLog).where(
	AuditLog.action == "DELETE"
)
```

## Campos Automáticos

### AuditMixin

Agrega a los modelos:
- `created_by`: UUID del usuario que creó el registro
- `updated_by`: UUID del usuario que modificó el registro por última vez

Estos campos se actualizan automáticamente mediante event listeners.

### TimestampMixin

Agrega:
- `created_at`: Timestamp de creación
- `updated_at`: Timestamp de última modificación

## Configuración Manual del Contexto

Si necesitas configurar el contexto manualmente:

```python
from core.audit import set_audit_context, clear_audit_context

# Configurar contexto
set_audit_context(
	user_id=user.id,
	user_email=user.email,
	ip_address="192.168.1.1",
	user_agent="Mozilla/5.0...",
	endpoint="/api/v1/providers",
	custom_field="valor personalizado"  # Metadatos adicionales
)

try:
	# Operaciones de BD
	await repository.save(provider)
finally:
	# Limpiar contexto
	clear_audit_context()
```

## Ejemplos de Consultas Avanzadas

### Ver Historial de Cambios de un Registro

```python
async def get_entity_history(entity_name: str, entity_id: str):
	"""Obtiene el historial completo de un registro"""
	query = select(AuditLog).where(
		AuditLog.entity_name == entity_name,
		AuditLog.entity_id == entity_id
	).order_by(AuditLog.timestamp.desc())

	result = await session.execute(query)
	return result.scalars().all()

# Uso
history = await get_entity_history("Provider", "123")
for log in history:
	print(f"{log.timestamp}: {log.action} by {log.user_email}")
	if log.action == "UPDATE":
		print(f"  Changed fields: {log.changed_fields}")
```

### Comparar Dos Versiones

```python
def compare_versions(old_log: AuditLog, new_log: AuditLog):
	"""Compara dos versiones de un registro"""
	changes = {}
	for field in new_log.changed_fields or []:
		changes[field] = {
			'old': old_log.new_values.get(field),
			'new': new_log.new_values.get(field)
		}
	return changes
```

### Auditoría por Período

```python
async def get_changes_by_period(start_date: datetime, end_date: datetime):
	"""Obtiene todos los cambios en un período"""
	query = select(AuditLog).where(
		AuditLog.timestamp >= start_date,
		AuditLog.timestamp <= end_date
	).order_by(AuditLog.timestamp.desc())

	result = await session.execute(query)
	return result.scalars().all()
```

## Migración de Base de Datos

Después de configurar el sistema, crear la migración:

```bash
# Crear migración
alembic revision --autogenerate -m "Add audit system"

# Revisar migración generada
# Editar si es necesario

# Aplicar migración
alembic upgrade head
```

## Rendimiento

### Optimizaciones

1. **Índices**: El modelo AuditLog incluye índices en:
   - `entity_name` + `entity_id`
   - `user_id`
   - `timestamp`

2. **Particionamiento** (para grandes volúmenes):
   - Considerar particionar la tabla por fecha
   - Archivar registros antiguos

3. **Exclusiones**: No auditar tablas de:
   - La propia tabla `audit_log`
   - Tablas temporales o de sesión
   - Logs o métricas

### Impacto

- **Espacio**: ~400-600 bytes por registro de auditoría
  - ID BIGSERIAL: 8 bytes (vs 16 bytes UUID)
  - JSONB: 20-40% más eficiente que JSON en PostgreSQL
- **Performance**: < 5ms overhead por operación de BD
  - Inserciones secuenciales optimizan índice B-tree
  - JSONB permite búsquedas rápidas con índices GIN
- **Escrituras**: 1 INSERT adicional por cambio

## Mejores Prácticas

### ✅ Hacer

1. **Auditar entidades críticas**: Proveedores, facturas, usuarios
2. **Establecer retención**: Definir política de retención de logs
3. **Monitorear tamaño**: Revisar periódicamente el tamaño de audit_log
4. **Usar índices**: Crear índices para consultas frecuentes
5. **Documentar acciones**: Agregar metadatos descriptivos cuando sea útil

### ❌ Evitar

1. **No auditar todo**: Solo auditar lo necesario
2. **No guardar contraseñas**: Excluir campos sensibles
3. **No consultar sin filtros**: Siempre usar WHERE en consultas
4. **No ignorar errores**: Monitorear fallos en auditoría

## Seguridad y Privacidad

### Datos Sensibles

Excluir campos sensibles de la auditoría:

```python
def _get_model_dict(instance: SQLModel, exclude_fields: set = None) -> dict:
	if exclude_fields is None:
		exclude_fields = {
			'created_at', 'updated_at',
			'created_by', 'updated_by',
			'password', 'password_hash',  # Nunca auditar contraseñas
			'token', 'secret_key'          # Ni tokens/secretos
		}
	# ...
```

### Acceso a Logs

Restringir acceso a audit_log:
- Solo administradores pueden consultar
- Implementar permissions en endpoints
- Registrar consultas a audit_log (meta-auditoría)

## Troubleshooting

### Los cambios no se registran

1. Verificar que el middleware esté configurado:
   ```python
   app.add_middleware(AuditMiddleware)
   ```

2. Verificar que setup_audit_listeners() se llamó:
   ```python
   from core.audit import setup_audit_listeners
   setup_audit_listeners()
   ```

3. Verificar que el modelo tenga un mixin auditable:
   ```python
   class MyModel(AuditMixin, SQLModel, table=True):
   ```

### created_by/updated_by es NULL

El usuario no está en el contexto. Verificar:

1. Que el middleware captura el usuario:
   ```python
   request.state.user = user
   ```

2. Que la autenticación se ejecuta antes del middleware de auditoría

### Performance degradado

1. Revisar índices en audit_log
2. Considerar particionamiento
3. Archivar logs antiguos
4. Limitar campos auditados

## Roadmap

Próximas mejoras:

- [ ] Dashboard de auditoría
- [ ] Exportación de logs a formatos externos
- [ ] Integración con sistemas SIEM
- [ ] Auditoría de consultas SELECT
- [ ] Restauración de versiones anteriores
- [ ] Alertas en tiempo real para cambios críticos

## Referencias

- [SQLAlchemy Events](https://docs.sqlalchemy.org/en/14/orm/events.html)
- [FastAPI Middleware](https://fastapi.tiangolo.com/tutorial/middleware/)
- [ContextVars](https://docs.python.org/3/library/contextvars.html)
