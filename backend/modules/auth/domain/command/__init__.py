from pydantic import BaseModel, Field


class RegisterUserDTO(BaseModel):
    email: str = Field(..., description="Email")
    nickname: str | None = Field(default=None, description="Nickname")
    name : str | None  = Field(default=None, description="Name")
    lastname : str | None = Field(default=None, description="Lastname")
    job_position : str | None = Field(default=None, description="Job Position")
    phone_number : str | None = Field(default=None, description="Phone Number")
    is_admin: bool = Field(default=False, description="Set as admin")
    is_owner: bool = Field(default=False, description="Set as super admin")