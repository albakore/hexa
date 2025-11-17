"""
Excepciones relacionadas con autenticación y autorización.
"""

from starlette import status
from core.exceptions.base import CustomException


class AuthenticationException(CustomException):
	"""Excepción base para errores de autenticación."""

	code = status.HTTP_401_UNAUTHORIZED
	error_code = "AUTHENTICATION_ERROR"
	message = "Authentication failed"


class AuthDecodeTokenException(CustomException):
	"""Token JWT no se puede decodificar (malformado o inválido)."""

	code = status.HTTP_401_UNAUTHORIZED
	error_code = "TOKEN__DECODE_ERROR"
	message = "Invalid token format"


class AuthExpiredTokenException(CustomException):
	"""Token JWT expirado."""

	code = status.HTTP_401_UNAUTHORIZED
	error_code = "TOKEN__EXPIRED"
	message = "Authentication token has expired"


class InvalidSignatureException(CustomException):
	"""Firma del token JWT inválida."""

	code = status.HTTP_401_UNAUTHORIZED
	error_code = "TOKEN__INVALID_SIGNATURE"
	message = "Invalid token signature"


class MissingAuthorizationException(CustomException):
	"""Header Authorization faltante."""

	code = status.HTTP_401_UNAUTHORIZED
	error_code = "MISSING_AUTHORIZATION"
	message = "Authorization header is required"


class InvalidAuthorizationFormatException(CustomException):
	"""Formato del header Authorization inválido."""

	code = status.HTTP_401_UNAUTHORIZED
	error_code = "INVALID_AUTHORIZATION_FORMAT"
	message = "Invalid authorization format. Expected: Bearer <token>"
