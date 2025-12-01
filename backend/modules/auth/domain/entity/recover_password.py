import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

from shared.mixins import TimestampMixin, AuditMixin

if TYPE_CHECKING:
	from modules.user.domain.entity import User


class RecoverPassword(SQLModel, TimestampMixin, AuditMixin, table=True):
	"""
	Entidad para gestionar las solicitudes de recuperación de contraseña.

	Esta entidad almacena las solicitudes de recuperación de contraseña
	de los usuarios, incluyendo el token, la nueva contraseña temporal
	y la fecha de expiración.
	"""

	id: uuid.UUID | None = Field(default_factory=uuid.uuid4, primary_key=True)
	fk_user: uuid.UUID = Field(foreign_key="user.id", nullable=False)
	new_password: str = Field(nullable=False)
	fecha_expiracion: datetime = Field(nullable=False)
	recovered: bool = Field(default=False, nullable=False)

	# Campo temporal (no persistido) para almacenar la contraseña en texto plano
	# Solo se usa para enviar el email, no se guarda en la base de datos
	temporary_password_plain: str | None = Field(default=None, sa_column=None)

	# Relación con User
	user: "User" = Relationship(back_populates="recover_passwords")
