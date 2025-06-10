from pydantic import BaseModel, Field


class GetUserListResponseDTO(BaseModel):
    id: int = Field(..., description="ID")
    email: str = Field(..., description="Email")
    nickname: str = Field(..., description="Nickname")


class CreateUserRequestDTO(BaseModel):
    email: str = Field(..., description="Email")
    nickname: str | None = Field(default=None, description="Nickname")
    name : str | None  = Field(default=None, description="Name")
    lastname : str | None = Field(default=None, description="Lastname")
    job_position : str | None = Field(default=None, description="Job Position")
    phone_number : str | None = Field(default=None, description="Phone Number")


class CreateUserResponseDTO(BaseModel):
    email: str = Field(..., description="Email")
    nickname: str = Field(..., description="Nickname")

class UserLoginResponseDTO(BaseModel):
    id: int | None = None
    nickname: str | None = None
    email: str | None = None
    name: str | None = None
    lastname: str | None = None
    job_position: str | None = None


class LoginResponseDTO(BaseModel):
    user: UserLoginResponseDTO
    token: str = Field(..., description="Token")
    refresh_token: str = Field(..., description="Refresh token")
