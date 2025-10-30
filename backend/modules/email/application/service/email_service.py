from dataclasses import dataclass
from typing import List, Dict, Any

from modules.email.domain.repository.email_repository import EmailRepository
from modules.email.domain.entity.email import Email
from modules.email.application.dto import SendEmailCommand, SendTemplateEmailCommand


@dataclass
class EmailService:
    """
    Servicio de aplicación para gestión de emails.

    Coordina el envío de emails usando el repositorio configurado.
    """

    email_repository: EmailRepository

    async def send_email(self, command: SendEmailCommand) -> bool:
        """
        Envía un email simple.

        Args:
            command: SendEmailCommand con los datos del email

        Returns:
            bool: True si se envió correctamente

        Raises:
            EmailSendException: Si ocurre un error al enviar
        """
        email = Email(
            to=command.to,
            subject=command.subject,
            body=command.body,
            from_email=command.from_email,
            cc=command.cc,
            bcc=command.bcc,
            is_html=command.is_html,
        )

        return await self.email_repository.send_email(email)

    async def send_template_email(self, command: SendTemplateEmailCommand) -> bool:
        """
        Envía un email usando un template con contenido dinámico.

        Args:
            command: SendTemplateEmailCommand con template y datos

        Returns:
            bool: True si se envió correctamente

        Raises:
            TemplateNotFoundException: Si el template no existe
            TemplateRenderException: Si falla el renderizado
            EmailSendException: Si ocurre un error al enviar
        """
        email = Email(
            to=command.to,
            subject=command.subject,
            body="",  # Se llenará con el template renderizado
            from_email=command.from_email,
            cc=command.cc,
            bcc=command.bcc,
            is_html=True,
            template_data=command.template_data,
        )

        return await self.email_repository.send_template_email(
            template_name=command.template_name,
            email=email
        )

    async def send_bulk_email(self, commands: List[SendEmailCommand]) -> Dict[str, Any]:
        """
        Envía múltiples emails en batch.

        Args:
            commands: Lista de SendEmailCommand

        Returns:
            Dict con estadísticas de envío: {
                "total": int,
                "success": int,
                "failed": int,
                "errors": List[str]
            }
        """
        results = {
            "total": len(commands),
            "success": 0,
            "failed": 0,
            "errors": []
        }

        for command in commands:
            try:
                await self.send_email(command)
                results["success"] += 1
            except Exception as e:
                results["failed"] += 1
                results["errors"].append(f"Error al enviar a {command.to}: {str(e)}")

        return results
