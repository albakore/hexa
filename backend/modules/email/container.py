from dependency_injector.containers import DeclarativeContainer, WiringConfiguration
from dependency_injector.providers import Singleton, Factory, Configuration

from core.config.settings import env
from modules.email.adapter.output.smtp_email_adapter import SMTPEmailAdapter
from modules.email.adapter.output.email_adapter import EmailAdapter
from modules.email.application.service.email_service import EmailService


class EmailContainer(DeclarativeContainer):
    """
    Contenedor de inyección de dependencias para el módulo Email.

    Configura y proporciona instancias de:
    - SMTPEmailAdapter: Implementación SMTP
    - EmailAdapter: Wrapper del repositorio
    - EmailService: Servicio de aplicación
    """

    wiring_config = WiringConfiguration(packages=["."], auto_wire=True)
    config = Configuration(pydantic_settings=[env])

    # Implementación SMTP concreta (Singleton)
    smtp_email_repository = Singleton(
        SMTPEmailAdapter,
        smtp_server=config.EMAIL_SMTP_SERVER,
        smtp_port=config.EMAIL_SMTP_PORT,
        smtp_username=config.EMAIL_SMTP_USERNAME,
        smtp_password=config.EMAIL_SMTP_PASSWORD,
        smtp_sender=config.EMAIL_SMTP_MAILSENDER,
        smtp_application=config.EMAIL_SMTP_APPLICATION,
        templates_dir=None,  # Usará el directorio por defecto
        use_tls=True,
    )

    # Adaptador wrapper (Factory)
    email_adapter = Factory(
        EmailAdapter,
        email_repository=smtp_email_repository
    )

    # Servicio de aplicación (Factory)
    service = Factory(
        EmailService,
        email_repository=email_adapter
    )
