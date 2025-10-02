from typing import List
from pydantic import BaseModel, Field

from modules.user.application.dto.user import UserLoginResponseDTO


class RefreshTokenResponse(BaseModel):
	user: UserLoginResponseDTO
	permissions: List[str]
	token: str = Field(..., description="Token")
	refresh_token: str = Field(..., description="Refresh token")
	is_admin: bool = Field(default=False, description="Is admin")
	is_owner: bool = Field(default=False, description="Is super admin")


class AuthPasswordResetResponse(BaseModel):
	status: str = "ok"
