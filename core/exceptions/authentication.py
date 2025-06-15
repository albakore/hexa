from core.exceptions.base import CustomException


class AuthDecodeTokenException(CustomException):
	code = 400
	error_code = "TOKEN__DECODE_ERROR"
	message = "token decode error"


class AuthExpiredTokenException(CustomException):
	code = 400
	error_code = "TOKEN__EXPIRE_TOKEN"
	message = "expired token"
