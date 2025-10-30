class EmailException(Exception):
    """Excepción base para errores relacionados con email"""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class EmailSendException(EmailException):
    """Excepción cuando falla el envío de un email"""
    pass


class TemplateNotFoundException(EmailException):
    """Excepción cuando no se encuentra un template"""
    pass


class TemplateRenderException(EmailException):
    """Excepción cuando falla el renderizado de un template"""
    pass
