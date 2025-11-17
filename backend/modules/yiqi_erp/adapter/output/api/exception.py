from core.exceptions import CustomException


class RequestException(CustomException):
	code = 500
	error_code = "REQUEST__ERROR_EXCEPTION"
	message = "Request error"

	def __init__(
		self, code=500, error_code="REQUEST__ERROR_EXCEPTION", message="Request error"
	):
		self.code = code
		self.error_code = error_code
		self.message = message
