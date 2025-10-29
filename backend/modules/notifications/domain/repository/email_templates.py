from abc import ABC, abstractmethod
from typing import Sequence
from modules.notifications.domain.entity import EmailTemplate

class EmailTemplateRepository(ABC):
    @abstractmethod
    async def get_all_email_templates(self) -> list[EmailTemplate] | Sequence[EmailTemplate]:
        ...

    @abstractmethod
    async def get_email_template_by_id(self, id: int) -> EmailTemplate | None:
        ...

    @abstractmethod
    async def get_email_template_by_name(self, name: str) -> EmailTemplate | None:
        ...    

    @abstractmethod
    async def get_email_template_by_module(self, module: str) -> EmailTemplate | None:
        ...

    @abstractmethod
    async def save_email_template(self, template: EmailTemplate) -> EmailTemplate:
        ...
    
    @abstractmethod
    async def delete_email_template(self, template: EmailTemplate) -> EmailTemplate | None:
        ...
