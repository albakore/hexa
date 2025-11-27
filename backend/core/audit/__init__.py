"""
Sistema de Auditoría para Fast Hexagonal

Este módulo proporciona un sistema completo de auditoría que registra
automáticamente todos los cambios (INSERT, UPDATE, DELETE) realizados
en las entidades marcadas como auditables.

Componentes principales:
- AuditLog: Modelo que almacena los registros de auditoría
- AuditMixin: Mixin para marcar modelos como auditables
- Context: Sistema de contexto para capturar el usuario actual
- Listeners: Event listeners que capturan cambios automáticamente

Uso básico:

1. Marcar un modelo como auditable:
	```python
	from shared.mixins import AuditMixin, TimestampMixin
	from sqlmodel import SQLModel, Field

	class MyModel(AuditMixin, TimestampMixin, SQLModel, table=True):
		id: int | None = Field(primary_key=True)
		name: str
	```

2. Configurar el contexto en cada request:
	```python
	from core.audit import set_audit_context

	@app.middleware("http")
	async def audit_middleware(request: Request, call_next):
		user = await get_current_user(request)

		set_audit_context(
			user_id=user.id,
			user_email=user.email,
			ip_address=request.client.host,
			user_agent=request.headers.get("user-agent"),
			endpoint=request.url.path
		)

		response = await call_next(request)

		clear_audit_context()
		return response
	```

3. Los cambios se registran automáticamente:
	```python
	# CREATE
	provider = Provider(name="ABC Corp")
	await repository.save(provider)
	# Se registra automáticamente en AuditLog: action=INSERT

	# UPDATE
	provider.name = "XYZ Corp"
	await repository.save(provider)
	# Se registra automáticamente en AuditLog: action=UPDATE

	# DELETE
	await repository.delete(provider)
	# Se registra automáticamente en AuditLog: action=DELETE
	```
"""

from core.audit.models import AuditLog
from core.audit.context import (
	set_audit_context,
	get_audit_context,
	clear_audit_context,
	get_current_user_id,
	get_current_user_email
)
from core.audit.listeners import setup_audit_listeners

__all__ = [
	'AuditLog',
	'set_audit_context',
	'get_audit_context',
	'clear_audit_context',
	'get_current_user_id',
	'get_current_user_email',
	'setup_audit_listeners'
]
