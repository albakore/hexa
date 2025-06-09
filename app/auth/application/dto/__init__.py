from pydantic import BaseModel, Field

from app.user.application.dto.user import CreateUserRequestDTO


class RefreshTokenResponseDTO(BaseModel):
    token: str = Field(..., description="Token")
    refresh_token: str = Field(..., description="Refresh token")

class AuthRegisterRequestDTO(CreateUserRequestDTO):
    ...
