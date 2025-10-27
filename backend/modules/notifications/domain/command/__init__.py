
import uuid
from pydantic import BaseModel


class CreateNotificationCommand(BaseModel):
    user_id: uuid.UUID | None = None    
    name: str = "user_registration"
    price: float = 0.0
    active: bool = True