from core.exceptions import CustomException


class EntityRelationShipNotFoundException(CustomException):
	code = 404
	error_code = "ENTITY_RELATIONSHIP__NOT_FOUND_ERROR"
	message = "Entity relationship not found"


class DuplicateAssociationException(CustomException):
	code = 400
	error_code = "DUPLICATE_ASSOCIATION__ERROR"
	message = "Entity already associated"


class EntityInstanceNotDeletedException(CustomException):
	code = 404
	error_code = "ENTITY_INSTANCE__NOT_FOUND_DELETE_ERROR"
	message = "Entity instance cannot be deleted"
