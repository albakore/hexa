import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from typing import Optional
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, TemplateNotFound, TemplateError

from modules.email.domain.repository.email_repository import EmailRepository
from modules.email.domain.entity.email import Email
from modules.email.domain.exception import (
    EmailSendException,
    TemplateNotFoundException,
    TemplateRenderException,
)


class SMTPEmailAdapter(EmailRepository):
    """
    Adaptador de salida para envío de emails usando SMTP nativo de Python.

    Implementa el envío de emails con soporte para:
    - Emails HTML y texto plano
    - Templates dinámicos con Jinja2
    - Archivos adjuntos
    - CC y BCC
    - SSL/TLS seguro
    """

    def __init__(
        self,
        smtp_server: str,
        smtp_port: int,
        smtp_username: str,
        smtp_password: str,
        smtp_sender: str,
        smtp_application: str,
        templates_dir: Optional[str] = None,
        use_tls: bool = True,
    ):
        """
        Inicializa el adaptador SMTP.

        Args:
            smtp_server: Servidor SMTP (ej: smtp.gmail.com)
            smtp_port: Puerto SMTP (ej: 587 para TLS, 465 para SSL)
            smtp_username: Usuario para autenticación SMTP
            smtp_password: Contraseña para autenticación SMTP
            smtp_sender: Email del remitente por defecto
            smtp_application: Nombre de la aplicación
            templates_dir: Directorio donde se encuentran los templates
            use_tls: Si se debe usar TLS (default: True)
        """
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.smtp_username = smtp_username
        self.smtp_password = smtp_password
        self.smtp_sender = smtp_sender
        self.smtp_application = smtp_application
        self.use_tls = use_tls

        # Configurar Jinja2 para templates
        if templates_dir:
            self.templates_dir = Path(templates_dir)
        else:
            # Por defecto, usar directorio templates dentro del módulo email
            self.templates_dir = Path(__file__).parent.parent.parent / "templates"

        self.jinja_env = None
        if self.templates_dir.exists():
            self.jinja_env = Environment(
                loader=FileSystemLoader(str(self.templates_dir)),
                autoescape=True
            )

    def _create_message(self, email: Email) -> MIMEMultipart:
        """
        Crea el mensaje MIME a partir de la entidad Email.

        Args:
            email: Entidad Email

        Returns:
            MIMEMultipart: Mensaje MIME configurado
        """
        message = MIMEMultipart("alternative")
        message["Subject"] = email.subject
        message["From"] = f"{self.smtp_application} <{email.from_email or self.smtp_sender}>"
        message["To"] = ", ".join(email.to)

        if email.cc:
            message["Cc"] = ", ".join(email.cc)

        # Agregar el cuerpo del email
        if email.is_html:
            part = MIMEText(email.body, "html", "utf-8")
        else:
            part = MIMEText(email.body, "plain", "utf-8")

        message.attach(part)

        # Agregar archivos adjuntos si existen
        if email.attachments:
            for attachment in email.attachments:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.content)
                encoders.encode_base64(part)
                part.add_header(
                    "Content-Disposition",
                    f"attachment; filename= {attachment.filename}",
                )
                message.attach(part)

        return message

    def _get_recipients(self, email: Email) -> list[str]:
        """
        Obtiene la lista completa de destinatarios (to, cc, bcc).

        Args:
            email: Entidad Email

        Returns:
            Lista de todos los destinatarios
        """
        recipients = email.to.copy()
        if email.cc:
            recipients.extend(email.cc)
        if email.bcc:
            recipients.extend(email.bcc)
        return recipients

    async def send_email(self, email: Email) -> bool:
        """
        Envía un email usando SMTP.

        Args:
            email: Entidad Email con los datos del correo

        Returns:
            bool: True si se envió correctamente

        Raises:
            EmailSendException: Si ocurre un error al enviar
        """
        try:
            message = self._create_message(email)
            recipients = self._get_recipients(email)

            # Crear conexión SMTP
            if self.use_tls:
                # Crear contexto SSL seguro
                context = ssl.create_default_context()
                with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                    server.starttls(context=context)
                    server.login(self.smtp_username, self.smtp_password)
                    server.sendmail(
                        email.from_email or self.smtp_sender,
                        recipients,
                        message.as_string()
                    )
            else:
                # Conexión SSL directa
                context = ssl.create_default_context()
                with smtplib.SMTP_SSL(
                    self.smtp_server,
                    self.smtp_port,
                    context=context
                ) as server:
                    server.login(self.smtp_username, self.smtp_password)
                    server.sendmail(
                        email.from_email or self.smtp_sender,
                        recipients,
                        message.as_string()
                    )

            return True

        except smtplib.SMTPException as e:
            raise EmailSendException(f"Error SMTP al enviar email: {str(e)}")
        except Exception as e:
            raise EmailSendException(f"Error inesperado al enviar email: {str(e)}")

    async def send_template_email(
        self,
        template_name: str,
        email: Email
    ) -> bool:
        """
        Envía un email usando un template con contenido dinámico.

        Args:
            template_name: Nombre del archivo template (ej: "welcome.html")
            email: Entidad Email con template_data para renderizar

        Returns:
            bool: True si se envió correctamente

        Raises:
            TemplateNotFoundException: Si el template no existe
            TemplateRenderException: Si falla el renderizado
            EmailSendException: Si ocurre un error al enviar
        """
        if not self.jinja_env:
            raise TemplateNotFoundException(
                f"No se ha configurado un directorio de templates"
            )

        try:
            # Cargar template
            template = self.jinja_env.get_template(template_name)

            # Renderizar template con datos dinámicos
            rendered_body = template.render(
                **(email.template_data or {})
            )

            # Crear nuevo email con el body renderizado
            email.body = rendered_body

            # Enviar email
            return await self.send_email(email)

        except TemplateNotFound:
            raise TemplateNotFoundException(
                f"Template '{template_name}' no encontrado en {self.templates_dir}"
            )
        except TemplateError as e:
            raise TemplateRenderException(
                f"Error al renderizar template '{template_name}': {str(e)}"
            )
