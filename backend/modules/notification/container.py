from dependency_injector.providers import Factory, Singleton
from dependency_injector.containers import DeclarativeContainer, WiringConfiguration

from modules.notification.adapter.output.persistence.email_template_adapter import EmailTemplateRepositoryAdapter
from modules.notification.adapter.output.persistence.notification_adapter import NotificationRepositoryAdapter
from modules.notification.adapter.output.persistence.postgres.email_template import PostgresEmailTemplateRepository
from modules.notification.adapter.output.persistence.postgres.notification import PostgresNotificationRepository
from modules.notification.application.service.email_template import EmailTemplateService
from modules.notification.application.service.notification import NotificationService


class NotificationContainer(DeclarativeContainer):
	wiring_config = WiringConfiguration(packages=["."], auto_wire=True)

	repository = Singleton(PostgresNotificationRepository)
	repository_adapter = Factory(NotificationRepositoryAdapter, notification_repository=repository)
	service = Factory(NotificationService, notification_repository=repository_adapter)

	email_template_repository = Singleton(PostgresEmailTemplateRepository)
	email_template_adapter = Factory(EmailTemplateRepositoryAdapter, email_template_repository=email_template_repository)
	email_template_service = Factory(EmailTemplateService, email_template_repository=email_template_adapter)
	