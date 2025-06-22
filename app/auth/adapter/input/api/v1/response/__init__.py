from typing import List
from pydantic import BaseModel, Field

from app.user.application.dto.user import UserLoginResponseDTO


class RefreshTokenResponse(BaseModel):
    user: UserLoginResponseDTO
    permissions: List[str]
    token: str = Field(..., description="Token")
    refresh_token: str = Field(..., description="Refresh token")

class AuthPasswordResetResponse(BaseModel):
    status: str = 'ok'