"""
Event listeners de SQLAlchemy para auditoría automática

Este módulo implementa listeners que capturan automáticamente
los eventos INSERT, UPDATE y DELETE de las entidades auditables.
"""

import json
import uuid
from datetime import date, datetime
from typing import Any

from sqlalchemy import event
from sqlalchemy.orm import Session
from sqlmodel import SQLModel

from core.audit.context import get_audit_context, get_current_user_id
from core.audit.models import AuditLog
from shared.mixins import AuditMixin


def _serialize_value(value: Any) -> Any:
	"""
	Serializa un valor para almacenarlo en JSON.

	Convierte tipos especiales (UUID, datetime, date) a strings.
	"""
	if isinstance(value, uuid.UUID):
		return str(value)
	elif isinstance(value, datetime):
		return value.isoformat()
	elif isinstance(value, date):
		return value.isoformat()
	elif hasattr(value, "__dict__"):
		# Para objetos complejos, intentar convertir a dict
		try:
			return str(value)
		except:
			return None
	return value


def _get_model_dict(instance: SQLModel, exclude_fields: set = None) -> dict:
	"""
	Convierte una instancia de modelo a diccionario.

	Args:
		instance: Instancia del modelo
		exclude_fields: Campos a excluir del diccionario

	Returns:
		Diccionario con los valores del modelo
	"""
	if exclude_fields is None:
		exclude_fields = {"created_at", "updated_at", "created_by", "updated_by"}

	result = {}
	for column in instance.__table__.columns:
		if column.name not in exclude_fields:
			value = getattr(instance, column.name, None)
			result[column.name] = _serialize_value(value)

	return result


def _get_entity_id(instance: SQLModel) -> str:
	"""
	Obtiene el ID de la entidad como string.

	Soporta diferentes tipos de claves primarias (int, UUID, str).
	"""
	# Buscar la columna de clave primaria
	pk_columns = [col for col in instance.__table__.columns if col.primary_key]

	if not pk_columns:
		return "unknown"

	pk_column = pk_columns[0]  # Tomar la primera clave primaria
	pk_value = getattr(instance, pk_column.name, None)

	return str(pk_value) if pk_value is not None else "unknown"


def _create_audit_log(
	session: Session,
	entity_name: str,
	entity_id: str,
	action: str,
	old_values: dict = None,
	new_values: dict = None,
):
	"""
	Crea un registro de auditoría.

	Args:
		session: Sesión de SQLAlchemy
		entity_name: Nombre de la entidad
		entity_id: ID de la entidad
		action: Tipo de acción (INSERT, UPDATE, DELETE)
		old_values: Valores anteriores (para UPDATE y DELETE)
		new_values: Valores nuevos (para INSERT y UPDATE)
	"""
	context = get_audit_context()

	# Calcular campos cambiados (solo para UPDATE)
	changed_fields = None
	if action == "UPDATE" and old_values and new_values:
		changed_fields = [
			field
			for field in new_values.keys()
			if old_values.get(field) != new_values.get(field)
		]

	audit_log = AuditLog(
		entity_name=entity_name,
		entity_id=entity_id,
		action=action,
		user_id=uuid.UUID(context["user_id"])
		if context and context.get("user_id")
		else None,
		user_email=context.get("user_email") if context else None,
		old_values=old_values,
		new_values=new_values,
		changed_fields=changed_fields,
		ip_address=context.get("ip_address") if context else None,
		user_agent=context.get("user_agent") if context else None,
		endpoint=context.get("endpoint") if context else None,
		extra_data=context.get("metadata") if context else None,
	)

	session.add(audit_log)


@event.listens_for(Session, "before_flush")
def receive_before_flush(session: Session, flush_context, instances):
	"""
	Listener que se ejecuta antes del flush de la sesión.

	Captura los cambios realizados en las entidades auditables y establece
	los campos de auditoría (created_by, updated_by).
	"""
	user_id = get_current_user_id()

	# Procesar nuevos objetos (INSERT)
	for obj in session.new:
		if isinstance(obj, AuditLog):
			# No auditar la tabla de auditoría
			continue

		if not isinstance(obj, SQLModel):
			continue

		# Verificar si es auditable
		is_auditable = hasattr(obj.__class__, "__mro__") and any(
			base.__name__ in ["AuditMixin", "TimestampMixin", "UserTimestampMixin"]
			for base in obj.__class__.__mro__
		)

		if not is_auditable:
			continue

		# Establecer created_by y updated_by si tiene AuditMixin
		if hasattr(obj, "created_by") and user_id:
			if not obj.created_by:
				obj.created_by = user_id

		if hasattr(obj, "updated_by") and user_id:
			if not obj.updated_by:
				obj.updated_by = user_id

	# Procesar objetos modificados (UPDATE)
	for obj in session.dirty:
		if not isinstance(obj, (SQLModel, AuditMixin)):
			continue

		if isinstance(obj, AuditLog):
			# No auditar la tabla de auditoría
			continue

		# Verificar si el modelo tiene el mixin de auditoría o timestamp
		is_auditable = hasattr(obj.__class__, "__mro__") and any(
			base.__name__ in ["AuditMixin", "TimestampMixin", "UserTimestampMixin"]
			for base in obj.__class__.__mro__
		)

		if not is_auditable:
			continue

		# Actualizar el campo updated_by si tiene AuditMixin
		if hasattr(obj, "updated_by") and user_id:
			obj.updated_by = user_id

		# Guardar estado antiguo para auditoría
		if not hasattr(session, "_audit_old_values"):
			session._audit_old_values = {}

		entity_id = _get_entity_id(obj)
		entity_name = obj.__class__.__name__

		# Usar el objeto tal como está antes del flush
		session._audit_old_values[(entity_name, entity_id)] = _get_model_dict(obj)


@event.listens_for(Session, "after_flush")
def receive_after_flush(session: Session, flush_context):
	"""
	Listener que se ejecuta después del flush de la sesión.

	Registra los cambios en la tabla de auditoría.
	"""
	# Procesar inserciones
	for obj in session.new:
		if isinstance(obj, AuditLog):
			# No auditar la tabla de auditoría
			continue

		if not isinstance(obj, SQLModel):
			continue

		# Verificar si es auditable
		is_auditable = hasattr(obj.__class__, "__mro__") and any(
			base.__name__ in ["AuditMixin", "TimestampMixin", "UserTimestampMixin"]
			for base in obj.__class__.__mro__
		)

		if not is_auditable:
			continue

		entity_name = obj.__class__.__name__
		entity_id = _get_entity_id(obj)
		new_values = _get_model_dict(obj)

		_create_audit_log(
			session=session,
			entity_name=entity_name,
			entity_id=entity_id,
			action="INSERT",
			new_values=new_values,
		)

	# Procesar actualizaciones
	for obj in session.dirty:
		if isinstance(obj, AuditLog):
			continue

		if not isinstance(obj, SQLModel):
			continue

		is_auditable = hasattr(obj.__class__, "__mro__") and any(
			base.__name__ in ["AuditMixin", "TimestampMixin", "UserTimestampMixin"]
			for base in obj.__class__.__mro__
		)

		if not is_auditable:
			continue

		entity_name = obj.__class__.__name__
		entity_id = _get_entity_id(obj)

		# Obtener valores viejos si fueron guardados
		old_values = None
		if hasattr(session, "_audit_old_values"):
			old_values = session._audit_old_values.get((entity_name, entity_id))

		new_values = _get_model_dict(obj)

		# Solo registrar si hubo cambios reales
		if old_values and old_values != new_values:
			_create_audit_log(
				session=session,
				entity_name=entity_name,
				entity_id=entity_id,
				action="UPDATE",
				old_values=old_values,
				new_values=new_values,
			)

	# Procesar eliminaciones
	for obj in session.deleted:
		if isinstance(obj, AuditLog):
			continue

		if not isinstance(obj, SQLModel):
			continue

		is_auditable = hasattr(obj.__class__, "__mro__") and any(
			base.__name__ in ["AuditMixin", "TimestampMixin", "UserTimestampMixin"]
			for base in obj.__class__.__mro__
		)

		if not is_auditable:
			continue

		entity_name = obj.__class__.__name__
		entity_id = _get_entity_id(obj)
		old_values = _get_model_dict(obj)

		_create_audit_log(
			session=session,
			entity_name=entity_name,
			entity_id=entity_id,
			action="DELETE",
			old_values=old_values,
		)

	# Limpiar valores antiguos almacenados
	if hasattr(session, "_audit_old_values"):
		session._audit_old_values.clear()


def setup_audit_listeners():
	"""
	Configura los event listeners de auditoría.

	Debe llamarse una vez al inicio de la aplicación.
	"""
	# Los listeners ya están configurados con los decoradores @event.listens_for
	# Esta función existe por si necesitamos configuración adicional
	pass
