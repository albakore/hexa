from core.exceptions.base import CustomException


class RegisteredUserException(CustomException):
    code = 400
    error_code = "REGISTERED_USER__ERROR_EXCEPTION"
    message = "User already registered"
 