from pydantic import BaseModel, Field


class GetUserListResponseDTO(BaseModel):
    id: int = Field(..., description="ID")
    email: str = Field(..., description="Email")
    nickname: str = Field(..., description="Nickname")


class CreateUserRequestDTO(BaseModel):
    email: str = Field(..., description="Email")
    nickname: str | None = Field(..., description="Nickname")
    name : str | None  = Field(..., description="Name")
    lastname : str | None = Field(..., description="Lastname")
    job_position : str | None = Field(..., description="Job Position")
    phone_number : int | None = Field(..., description="Phone Number")


class CreateUserResponseDTO(BaseModel):
    email: str = Field(..., description="Email")
    nickname: str = Field(..., description="Nickname")


class LoginResponseDTO(BaseModel):
    token: str = Field(..., description="Token")
    refresh_token: str = Field(..., description="Refresh token")
