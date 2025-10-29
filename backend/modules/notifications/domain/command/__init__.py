import html
import uuid
from pydantic import BaseModel

class CreateNotificationCommand(BaseModel):
    user_id: uuid.UUID | None = None    
    name: str = "user_registration"
    price: float = 0.0
    active: bool = True
    
class EditEmailTemplateCommand(BaseModel):
    name: str | None = None
    description: str | None = None
    template_html: bytes | None = None
    module: str | None = None
