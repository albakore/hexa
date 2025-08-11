from core.exceptions import CustomException

class CurrencyNotFoundException(CustomException):
	code = 404
	error_code = "CURRENCY__NOT_FOUND_ERROR"
	message = "Currency not found"