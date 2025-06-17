from core.exceptions import CustomException

class RoleNotFoundException(CustomException):
    code = 404
    error_code = "ROLE__NOT_FOUND_ERROR"
    message = "Role not found"

class PermissionNotFoundException(CustomException):
    code = 404
    error_code = "PERMISSION__NOT_FOUND_ERROR"
    message = "Permission not found"