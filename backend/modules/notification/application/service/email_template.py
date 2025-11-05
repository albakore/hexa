from dataclasses import dataclass

from modules.notification.domain.command import EditEmailTemplateCommand
from modules.notification.domain.entity.email_template import EmailTemplate
from modules.notification.domain.exception import EmailTemplateNotFoundException
from modules.notification.domain.repository.email_template import EmailTemplateRepository
from modules.notification.domain.repository.sender_provider import SenderProviderPort
from modules.notification.domain.usecase.email_template import EmailTemplateUseCaseFactory


@dataclass
class EmailTemplateService:
    
    email_template_repository : EmailTemplateRepository
    email_template_sender: SenderProviderPort

    def __post_init__(self):
        self.usecase = EmailTemplateUseCaseFactory(self.email_template_repository, self.email_template_sender)

    async def get_all_email_templates(self):
        email_templates = await self.usecase.get_all_email_templates()
        return email_templates
    
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

    # async def send_email_template(self, receiver_email: list[str], subject: str, body: str):
    #     await self.usecase.send_email_template(receiver_email, subject, body)
