from dependency_injector.providers import Factory, Singleton
from dependency_injector.containers import DeclarativeContainer, WiringConfiguration
from dependency_injector.providers import Configuration
from core.config.settings import env

from modules.notification.adapter.output.email.email_sender import EmailSender
from modules.notification.adapter.output.persistence.email_template_adapter import (
	EmailTemplateRepositoryAdapter,
)
from modules.notification.adapter.output.persistence.notification_adapter import (
	NotificationRepositoryAdapter,
)
from modules.notification.adapter.output.persistence.postgres.email_template import (
	PostgresEmailTemplateRepository,
)
from modules.notification.adapter.output.persistence.postgres.notification import (
	PostgresNotificationRepository,
)
from modules.notification.adapter.output.slack.slack_sender import SlackSender
from modules.notification.application.service.email_template import EmailTemplateService
from modules.notification.application.service.notification import NotificationService


class NotificationContainer(DeclarativeContainer):
	wiring_config = WiringConfiguration(packages=["."], auto_wire=True)

	config = Configuration(pydantic_settings=[env])

	email_sender = Singleton(
		EmailSender,
		config.EMAIL_SMTP_SERVER,
		config.EMAIL_SMTP_PORT,
		config.EMAIL_SMTP_USERNAME,
		config.EMAIL_SMTP_PASSWORD,
		config.EMAIL_SMTP_MAILSENDER,
	)

	slack_sender = Singleton(
		SlackSender,
		config.WEBHOOK_SLACK_NOTIFY_MLA,
		config.WEBHOOK_SLACK_API_TOKEN_MLA
	)

	repository = Singleton(PostgresNotificationRepository)
	repository_adapter = Factory(
		NotificationRepositoryAdapter, notification_repository=repository
	)

	email_template_repository = Singleton(PostgresEmailTemplateRepository)
	email_template_adapter = Factory(
		EmailTemplateRepositoryAdapter,
		email_template_repository=email_template_repository,
	)
	email_template_service = Factory(
		EmailTemplateService,
		email_template_repository=email_template_adapter,
		email_template_sender=email_sender,
	)
	
	service = Factory(
		NotificationService,
		notification_repository=repository_adapter,
		sender_providers={
			"email": email_sender,
			"slack": slack_sender,
		},
		email_template_service=email_template_service
	)
