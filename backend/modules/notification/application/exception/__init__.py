from core.exceptions.base import CustomException


class ProviderSenderNotFoundException(CustomException):
	code = 404
	error_code = "PROVIDER_SENDER__NOT_FOUND_EXCEPTION"
	message = "No existe el provedor de envio de notificacion"
