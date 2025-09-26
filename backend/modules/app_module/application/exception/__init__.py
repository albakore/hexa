from core.exceptions import CustomException


class ModuleNotFoundException(CustomException):
	code = 404
	error_code = "MODULE__NOT_FOUND_ERROR"
	message = "Module not found"
