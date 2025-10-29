from typing import Sequence
from core.db.session import session_factory, session as global_session
from sqlmodel import select

from modules.notifications.domain.entity import EmailTemplate
from modules.notifications.domain.repository.email_templates import EmailTemplateRepository

class PostgresEmailTemplateRepository(EmailTemplateRepository):
    async def get_all_email_templates(self) -> list[EmailTemplate] | Sequence[EmailTemplate]:
        query = select(EmailTemplate)

        async with session_factory() as session:
            result = await session.execute(query)
        return result.scalars().all()

    async def get_email_template_by_id(self, id: int) -> EmailTemplate | None:
        query = select(EmailTemplate).where(EmailTemplate.id == id)

        async with session_factory() as session:
            result = await session.execute(query)
        return result.scalars().first()

    async def get_email_template_by_name(self, name: str) -> EmailTemplate | None:
        query = select(EmailTemplate).where(EmailTemplate.name == name)

        async with session_factory() as session:
            result = await session.execute(query)
        return result.scalars().first()

    async def get_email_template_by_module(self, module: str) -> EmailTemplate | None:
        query = select(EmailTemplate).where(EmailTemplate.module == module)

        async with session_factory() as session:
            result = await session.execute(query)
        return result.scalars().first()

    async def save_email_template(self, template: EmailTemplate) -> EmailTemplate:
        global_session.add(template)
        await global_session.flush()
        return template

    async def delete_email_template(self, template: EmailTemplate) -> EmailTemplate | None:
        await global_session.delete(template)
        await global_session.flush()
        return template
