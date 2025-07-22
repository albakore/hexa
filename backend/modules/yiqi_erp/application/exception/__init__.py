from core.exceptions import CustomException


class YiqiServiceException(CustomException):
	code = 500
	error_code = "YIQI__SERVICE_ERROR"
	message = "Hubo un error al contactar con el servicio externo de yiqi"