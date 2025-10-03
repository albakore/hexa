from core.exceptions import CustomException


class LoginUsernamePasswordException(CustomException):
	code = 400
	error_code = "LOGIN__USER_PASSWORD_ERROR"
	message = "Incorrect username/password"


class LoginRequiresPasswordResetException(CustomException):
	code = 400
	error_code = "LOGIN__REQUIRES_PASSWORD_RESET"
	message = "User requires password reset"


class DecodeTokenException(CustomException):
	code = 400
	error_code = "TOKEN__DECODE_ERROR"
	message = "token decode error"


class ExpiredTokenException(CustomException):
	code = 400
	error_code = "TOKEN__EXPIRE_TOKEN"
	message = "expired token"


class AuthPasswordResetError(CustomException):
	code = 400
	error_code = "AUTH__PASSWORD_RESET_ERROR"
	message = "Password reset error"


class AuthInitialPasswordResetError(CustomException):
	code = 400
	error_code = "AUTH__INITIAL_PASSWORD_RESET_ERROR"
	message = "Initial password reset error"


class AuthSessionExpiredException(CustomException):
	code = 400
	error_code = "AUTH__SESSION_EXPIRED_ERROR"
	message = "Session expired for user, please login"
