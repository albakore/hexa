from abc import ABC, abstractmethod
from typing import Optional
from modules.email.domain.entity.email import Email


class EmailRepository(ABC):
    """
    Repositorio abstracto para el envío de emails.

    Define la interfaz que deben implementar los adaptadores de salida
    para el envío de correos electrónicos.
    """

    @abstractmethod
    async def send_email(self, email: Email) -> bool:
        """
        Envía un email.

        Args:
            email: Entidad Email con los datos del correo a enviar

        Returns:
            bool: True si el email se envió correctamente, False en caso contrario

        Raises:
            EmailSendException: Si ocurre un error al enviar el email
        """
        pass

    @abstractmethod
    async def send_template_email(
        self,
        template_name: str,
        email: Email
    ) -> bool:
        """
        Envía un email usando un template con contenido dinámico.

        Args:
            template_name: Nombre del template a usar
            email: Entidad Email con los datos del correo y template_data

        Returns:
            bool: True si el email se envió correctamente, False en caso contrario

        Raises:
            EmailSendException: Si ocurre un error al enviar el email
            TemplateNotFoundException: Si el template no existe
        """
        pass
