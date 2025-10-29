from dependency_injector.providers import Factory, Singleton
from dependency_injector.containers import DeclarativeContainer, WiringConfiguration

from modules.notifications.adapter.output.persistence.email_template_adapter import EmailTemplateRepositoryAdapter
from modules.notifications.adapter.output.persistence.notification_adapter import NotificationRepositoryAdapter
from modules.notifications.adapter.output.persistence.postgres.email_templates import PostgresEmailTemplateRepository
from modules.notifications.adapter.output.persistence.postgres.notifications import PostgresNotificationRepository
from modules.notifications.application.service.email_templates import EmailTemplateService
from modules.notifications.application.service.notifications import NotificationService

class NotificationsContainer(DeclarativeContainer):
	wiring_config = WiringConfiguration(packages=["."], auto_wire=True)

	repository = Singleton(PostgresNotificationRepository)
	repository_adapter = Factory(NotificationRepositoryAdapter, notification_repository=repository)
	service = Factory(NotificationService, notification_repository=repository_adapter)

	email_template_repository = Singleton(PostgresEmailTemplateRepository)
	email_template_adapter = Factory(EmailTemplateRepositoryAdapter, email_template_repository=email_template_repository)
	email_template_service = Factory(EmailTemplateService, email_template_repository=email_template_adapter)
	