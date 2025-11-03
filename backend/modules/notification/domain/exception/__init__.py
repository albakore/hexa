from core.exceptions import CustomException

class NotificationNotFoundException(CustomException):
    code = 404
    error_code = "NOTIFICATION__NOT_FOUND_ERROR"
    message = "Notification not found"

class EmailTemplateNotFoundException(CustomException):
    code = 404
    error_code = "EMAIL_TEMPLATE__NOT_FOUND_ERROR"
    message = "Email template not found"
