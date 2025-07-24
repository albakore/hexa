from core.exceptions import CustomException


class EntityRelationShipNotFoundException(CustomException):
	code = 404
	error_code = "ENTITY_RELATIONSHIP__NOT_FOUND_ERROR"
	message = "Entity relationship not found"