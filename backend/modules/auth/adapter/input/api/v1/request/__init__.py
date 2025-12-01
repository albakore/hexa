import uuid
from pydantic import BaseModel, Field

from modules.auth.application.dto import AuthRegisterRequestDTO


class RefreshTokenRequest(BaseModel):
	# token: str = Field(..., description="Token")
	refresh_token: str = Field(..., description="Refresh token")


class VerifyTokenRequest(BaseModel):
	token: str = Field(..., description="Token")


class AuthLoginRequest(BaseModel):
	nickname: str = Field(..., description="nickname or email")
	password: str


class AuthRegisterRequest(AuthRegisterRequestDTO): ...


class AuthPasswordResetRequest(BaseModel):
	id: uuid.UUID = Field(..., description="User ID")
	initial_password: str = Field(..., description="Initial password")
	new_password: str = Field(..., description="New password account")


class AuthRecoveryPasswordRequest(BaseModel):
	email_or_nickname: str = Field(..., description="Email or nickname of the user")


class AuthCompleteRecoveryPasswordRequest(BaseModel):
	email_or_nickname: str = Field(..., description="Email or nickname of the user")
	temporary_password: str = Field(..., description="Temporary password received by email")
	new_password: str = Field(..., description="New password chosen by the user")
