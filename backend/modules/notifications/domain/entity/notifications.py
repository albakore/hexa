import uuid
from sqlmodel import SQLModel, Field

class Notification(SQLModel, table=True):
    id: int|None = Field(default=None, primary_key=True)
    user_id: uuid.UUID | None = Field(default=None)
    name: str = ""
    price: float = 0.0 #TODO: quizás reemplazar por otro parametro más relevante
    active: bool = True
    