from core.exceptions import CustomException


class LoginUsernamePasswordException(CustomException):
    code = 400
    error_code = "LOGIN__USER_PASSWORD_ERROR"
    message = "token decode error"

class DecodeTokenException(CustomException):
    code = 400
    error_code = "TOKEN__DECODE_ERROR"
    message = "token decode error"


class ExpiredTokenException(CustomException):
    code = 400
    error_code = "TOKEN__EXPIRE_TOKEN"
    message = "expired token"