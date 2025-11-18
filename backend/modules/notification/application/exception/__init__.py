from core.exceptions.base import CustomException


class ProviderSenderNotFoundException(CustomException):
	code = 404
	error_code = "PROVIDER_SENDER__NOT_FOUND_EXCEPTION"
	message = "No existe el provedor de envio de notificacion"


class NullEmailTemplateHTMLException(CustomException):
	code = 404
	error_code = "EMAIL_TEMPLATE__HTML_NULL_EXCEPTION"
	message = "El template no tiene cargado el html"
