from dataclasses import dataclass
from typing import Sequence

from modules.notification.domain.entity import EmailTemplate
from modules.notification.domain.repository.email_template import EmailTemplateRepository


@dataclass
class EmailTemplateRepositoryAdapter(EmailTemplateRepository):
    email_template_repository: EmailTemplateRepository

    async def get_all_email_templates(self) -> list[EmailTemplate] | Sequence[EmailTemplate]:
        return await self.email_template_repository.get_all_email_templates()

    async def get_email_template_by_id(self, id: int) -> EmailTemplate | None:
        return await self.email_template_repository.get_email_template_by_id(id)

    async def get_email_template_by_name(self, name: str) -> EmailTemplate | None:
        return await self.email_template_repository.get_email_template_by_name(name)

    async def get_email_template_by_module(self, module: str) -> EmailTemplate | None:
        return await self.email_template_repository.get_email_template_by_module(module)

    async def save_email_template(self, template: EmailTemplate) -> EmailTemplate:
        return await self.email_template_repository.save_email_template(template)

    async def delete_email_template(self, template: EmailTemplate) -> EmailTemplate | None:
        return await self.email_template_repository.delete_email_template(template)

