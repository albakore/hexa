import uuid
from pydantic import BaseModel, Field

from modules.user.application.dto import LoginResponseDTO
from modules.user.application.dto.user import CreateUserRequestDTO


class RefreshTokenResponseDTO(LoginResponseDTO):
	token: str = Field(..., description="Token")
	refresh_token: str = Field(..., description="Refresh token")


class AuthRegisterRequestDTO(CreateUserRequestDTO): ...


class AuthPasswordResetResponseDTO(BaseModel):
	id: uuid.UUID
