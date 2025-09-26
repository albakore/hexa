from core.exceptions import CustomException


class PasswordDoesNotMatchException(CustomException):
	code = 401
	error_code = "USER__PASSWORD_DOES_NOT_MATCH"
	message = "password does not match"


class DuplicateEmailOrNicknameException(CustomException):
	code = 400
	error_code = "USER__DUPLICATE_EMAIL_OR_NICKNAME"
	message = "duplicate email or nickname"


class UserNotFoundException(CustomException):
	code = 404
	error_code = "USER__NOT_FOUND"
	message = "user not found"


class UserRegisteredException(CustomException):
	code = 400
	error_code = "USER__REGISTERER_FOUND"
	message = "The user has been previously registered"


class UserInactiveException(CustomException):
	code = 400
	error_code = "USER__INACTIVE"
	message = "User Inactive"
