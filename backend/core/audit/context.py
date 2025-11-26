"""
Contexto de auditoría para capturar información del usuario actual

Este módulo proporciona un contexto global que almacena información
del usuario actual durante el ciclo de vida de una request.
"""

from contextvars import ContextVar
from typing import Optional
import uuid


# ContextVar para almacenar información del usuario actual
_audit_context: ContextVar[Optional[dict]] = ContextVar('audit_context', default=None)


def set_audit_context(
	user_id: Optional[uuid.UUID] = None,
	user_email: Optional[str] = None,
	ip_address: Optional[str] = None,
	user_agent: Optional[str] = None,
	endpoint: Optional[str] = None,
	**kwargs
):
	"""
	Establece el contexto de auditoría para el request actual.

	Args:
		user_id: UUID del usuario autenticado
		user_email: Email del usuario autenticado
		ip_address: Dirección IP del cliente
		user_agent: User agent del navegador
		endpoint: Endpoint de la API que se está ejecutando
		**kwargs: Metadatos adicionales personalizados

	Ejemplo:
		set_audit_context(
			user_id=user.id,
			user_email=user.email,
			ip_address=request.client.host,
			user_agent=request.headers.get("user-agent"),
			endpoint=request.url.path
		)
	"""
	context = {
		'user_id': str(user_id) if user_id else None,
		'user_email': user_email,
		'ip_address': ip_address,
		'user_agent': user_agent,
		'endpoint': endpoint,
		'metadata': kwargs
	}
	_audit_context.set(context)


def get_audit_context() -> Optional[dict]:
	"""
	Obtiene el contexto de auditoría actual.

	Returns:
		Diccionario con la información del contexto o None si no está establecido
	"""
	return _audit_context.get()


def clear_audit_context():
	"""
	Limpia el contexto de auditoría actual.

	Debe llamarse al final de cada request para evitar fugas de información.
	"""
	_audit_context.set(None)


def get_current_user_id() -> Optional[str]:
	"""
	Obtiene el ID del usuario actual del contexto.

	Returns:
		UUID del usuario como string o None
	"""
	context = get_audit_context()
	return context.get('user_id') if context else None


def get_current_user_email() -> Optional[str]:
	"""
	Obtiene el email del usuario actual del contexto.

	Returns:
		Email del usuario o None
	"""
	context = get_audit_context()
	return context.get('user_email') if context else None
