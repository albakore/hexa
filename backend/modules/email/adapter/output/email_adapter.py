from modules.email.domain.repository.email_repository import EmailRepository
from modules.email.domain.entity.email import Email


class EmailAdapter(EmailRepository):
    """
    Adaptador wrapper para el repositorio de email.

    Permite cambiar la implementación concreta sin afectar al resto del sistema.
    """

    def __init__(self, email_repository: EmailRepository):
        self.email_repository = email_repository

    async def send_email(self, email: Email) -> bool:
        """Envía un email usando el repositorio configurado"""
        return await self.email_repository.send_email(email)

    async def send_template_email(
        self,
        template_name: str,
        email: Email
    ) -> bool:
        """Envía un email con template usando el repositorio configurado"""
        return await self.email_repository.send_template_email(template_name, email)
