from core.exceptions import CustomException


class OutputPortException(CustomException):
	code = 500
	error_code = "OUTPUT_PORT_ENTITY_CLASS__INTERNAL_ERROR"
	message = "El tipo de entidad no es compatible con el controlador actual"
	
class EntityInstanceNotFoundException(CustomException):
	code = 404
	error_code = "ENTITY_INSTANCE__NOT_FOUND_ERROR"
	message = "Entity instance not found"
	