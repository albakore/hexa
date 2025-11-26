"""
Mixins reutilizables para modelos SQLModel/SQLAlchemy

Este módulo proporciona mixins que agregan funcionalidad común a los modelos,
como campos de timestamp y auditoría que se actualizan automáticamente.

IMPORTANTE: Los mixins ahora usan Field() de SQLModel en lugar de @declared_attr
para garantizar compatibilidad completa con SQLModel.
"""

import warnings
from datetime import datetime
from typing import Optional

from sqlalchemy import func
from sqlalchemy.exc import SAWarning
from sqlmodel import Field

# Silenciar warnings de SQLAlchemy sobre acceso a atributos declarativos
# Estos warnings aparecen cuando se importan modelos que usan mixins
# fuera del contexto de una sesión de base de datos
warnings.filterwarnings(
	"ignore",
	message=".*Unmanaged access of declarative attribute.*",
	category=SAWarning,
)


class TimestampMixin:
	"""
	Mixin que agrega campos de timestamp a los modelos.

	Campos:
	- created_at: Fecha y hora de creación del registro (auto)
	- updated_at: Fecha y hora de última modificación (auto)

	Uso:
		class MyModel(SQLModel, TimestampMixin, table=True):
			id: int | None = Field(primary_key=True)
			name: str
			# created_at y updated_at se agregan automáticamente
	"""

	created_at: Optional[datetime] = Field(
		default=None,
		sa_column_kwargs={
			"server_default": func.now(),
			"nullable": False,
		},
	)

	updated_at: Optional[datetime] = Field(
		default=None,
		sa_column_kwargs={
			"server_default": func.now(),
			"onupdate": func.now(),
			"nullable": False,
		},
	)


class UserTimestampMixin:
	"""
	Mixin específico para modelos de usuario que agrega campos de sesión.

	Campos:
	- date_registration: Fecha de registro del usuario
	- date_last_session: Fecha de última sesión del usuario
	- created_at: Fecha y hora de creación del registro (auto)
	- updated_at: Fecha y hora de última modificación (auto)

	Uso:
		class User(SQLModel, UserTimestampMixin, table=True):
			id: uuid.UUID = Field(primary_key=True)
			email: str
			# campos de timestamp se agregan automáticamente
	"""

	date_registration: Optional[datetime] = Field(
		default=None,
		sa_column_kwargs={
			"server_default": func.now(),
			"nullable": False,
		},
	)

	date_last_session: Optional[datetime] = Field(
		default=None,
		sa_column_kwargs={
			"nullable": True,
		},
	)

	created_at: Optional[datetime] = Field(
		default=None,
		sa_column_kwargs={
			"server_default": func.now(),
			"nullable": False,
		},
	)

	updated_at: Optional[datetime] = Field(
		default=None,
		sa_column_kwargs={
			"server_default": func.now(),
			"onupdate": func.now(),
			"nullable": False,
		},
	)


class SoftDeleteMixin:
	"""
	Mixin que agrega funcionalidad de soft delete (borrado lógico).

	Campos:
	- deleted_at: Fecha y hora de eliminación (null si no está eliminado)
	- is_deleted: Bandera booleana que indica si está eliminado

	Uso:
		class MyModel(SQLModel, SoftDeleteMixin, TimestampMixin, table=True):
			id: int | None = Field(primary_key=True)
			name: str
			# campos de soft delete se agregan automáticamente
	"""

	deleted_at: Optional[datetime] = Field(
		default=None,
		sa_column_kwargs={
			"nullable": True,
		},
	)

	is_deleted: bool = Field(
		default=False,
		sa_column_kwargs={
			"nullable": False,
		},
	)


class AuditMixin:
	"""
	Mixin que agrega campos de auditoría a los modelos.

	Campos:
	- created_by: UUID del usuario que creó el registro (como string)
	- updated_by: UUID del usuario que modificó el registro por última vez (como string)

	Estos campos se actualizan automáticamente mediante event listeners.

	Uso:
		class MyModel(SQLModel, AuditMixin, TimestampMixin, table=True):
			id: int | None = Field(primary_key=True)
			name: str
			# created_by y updated_by se agregan automáticamente

	Nota: Para que funcione correctamente, debe configurarse el contexto
	de auditoría en cada request con set_audit_context().
	"""

	created_by: Optional[str] = Field(
		default=None,
		max_length=36,
		sa_column_kwargs={
			"nullable": True,
		},
	)

	updated_by: Optional[str] = Field(
		default=None,
		max_length=36,
		sa_column_kwargs={
			"nullable": True,
		},
	)
