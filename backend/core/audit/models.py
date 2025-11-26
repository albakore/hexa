"""
Modelos para el sistema de auditoría

Este módulo define el modelo AuditLog que registra todos los cambios
realizados en las entidades auditables de la aplicación.
"""

import uuid
from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field, Column
from sqlalchemy import DateTime, func, Text
from sqlalchemy.dialects.postgresql import JSONB


class AuditLog(SQLModel, table=True):
	"""
	Modelo de registro de auditoría.

	Registra todos los cambios (INSERT, UPDATE, DELETE) realizados
	en las entidades marcadas como auditables.

	Campos:
	- id: ID incremental del registro de auditoría (BIGSERIAL)
	- entity_name: Nombre de la entidad/tabla modificada
	- entity_id: ID del registro modificado
	- action: Tipo de acción (INSERT, UPDATE, DELETE)
	- user_id: ID del usuario que realizó el cambio
	- user_email: Email del usuario (desnormalizado para consultas rápidas)
	- timestamp: Fecha y hora del cambio
	- old_values: Valores anteriores (solo para UPDATE y DELETE)
	- new_values: Valores nuevos (solo para INSERT y UPDATE)
	- changed_fields: Lista de campos que cambiaron (solo para UPDATE)
	- ip_address: Dirección IP del cliente
	- user_agent: User agent del navegador/cliente
	- endpoint: Endpoint de la API que generó el cambio
	"""

	__tablename__ = "audit_log"

	id: int | None = Field(
		default=None,
		primary_key=True,
		description="ID incremental del registro de auditoría (BIGSERIAL en PostgreSQL)"
	)

	# Información de la entidad
	entity_name: str = Field(
		max_length=100,
		description="Nombre de la entidad/tabla modificada"
	)
	entity_id: str = Field(
		max_length=100,
		description="ID del registro modificado (como string para flexibilidad)"
	)

	# Tipo de acción
	action: str = Field(
		max_length=10,
		description="Tipo de acción: INSERT, UPDATE, DELETE"
	)

	# Información del usuario
	user_id: Optional[uuid.UUID] = Field(
		default=None,
		description="ID del usuario que realizó el cambio"
	)
	user_email: Optional[str] = Field(
		default=None,
		max_length=255,
		description="Email del usuario (desnormalizado)"
	)

	# Timestamp
	timestamp: datetime = Field(
		sa_column=Column(
			DateTime(timezone=True),
			server_default=func.now(),
			nullable=False
		),
		description="Fecha y hora del cambio"
	)

	# Datos del cambio
	old_values: Optional[dict] = Field(
		default=None,
		sa_column=Column(JSONB),
		description="Valores anteriores del registro (JSONB)"
	)
	new_values: Optional[dict] = Field(
		default=None,
		sa_column=Column(JSONB),
		description="Valores nuevos del registro (JSONB)"
	)
	changed_fields: Optional[list] = Field(
		default=None,
		sa_column=Column(JSONB),
		description="Lista de campos que cambiaron"
	)

	# Contexto adicional
	ip_address: Optional[str] = Field(
		default=None,
		max_length=45,
		description="Dirección IP del cliente (IPv4 o IPv6)"
	)
	user_agent: Optional[str] = Field(
		default=None,
		sa_column=Column(Text),
		description="User agent del navegador/cliente"
	)
	endpoint: Optional[str] = Field(
		default=None,
		max_length=255,
		description="Endpoint de la API que generó el cambio"
	)

	# Información adicional (flexible)
	extra_data: Optional[dict] = Field(
		default=None,
		sa_column=Column(JSONB),
		description="Datos adicionales personalizados en formato JSONB"
	)
