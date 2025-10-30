"""
Módulo Email - Configuración del módulo

Este archivo define el módulo Email y su integración con el sistema.
"""

from modules.email.container import EmailContainer


def get_container():
    """Retorna el contenedor de dependencias del módulo Email"""
    return EmailContainer()


# Metadata del módulo
MODULE_NAME = "email"
MODULE_DESCRIPTION = "Módulo para envío de correos electrónicos con soporte SMTP y templates"
MODULE_VERSION = "1.0.0"
