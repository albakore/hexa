from dataclasses import dataclass

from modules.notifications.domain.command import EditEmailTemplateCommand
from modules.notifications.domain.entity.email_templates import EmailTemplate
from modules.notifications.domain.exception import EmailTemplateNotFoundException
from modules.notifications.domain.repository.email_templates import EmailTemplateRepository
from modules.notifications.domain.usecase.email_templates import EmailTemplatesUseCaseFactory

@dataclass
class EmailTemplateService:
    
    email_template_repository : EmailTemplateRepository

    def __post_init__(self):
        self.usecase = EmailTemplatesUseCaseFactory(self.email_template_repository)

    async def get_all_email_templates(self):
        email_template = await self.usecase.get_all_email_templates()
        return email_template
    
    async def get_email_template_by_id(self, id: int):
        email_template = await self.usecase.get_email_template_by_id(id)
        return email_template
    
    async def get_email_template_by_name(self, name: str):
        email_template = await self.usecase.get_email_template_by_name(name)
        return email_template
    
    async def get_email_template_by_module(self, module: str):
        email_template = await self.usecase.get_email_template_by_module(module)
        return email_template
    
    async def save_email_template(self, template: EmailTemplate):
        new_email_template = await self.usecase.save_email_template(template)
        return new_email_template

    async def edit_email_template(self, id: int, command: EditEmailTemplateCommand):
        #TODO: minificar acá y no en la capa de adaptador
        email_template = await self.usecase.get_email_template_by_id(id)
        if not email_template:
            raise EmailTemplateNotFoundException
        email_template.sqlmodel_update(command.model_dump(exclude_unset=True, exclude_none=True))
        edited_email_template = await self.usecase.save_email_template(email_template)
        return edited_email_template
    
    async def delete_email_template(self, id: int):
        await self.usecase.delete_email_template(id)
    