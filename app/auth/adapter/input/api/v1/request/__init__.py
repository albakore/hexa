from pydantic import BaseModel, Field

from app.auth.application.dto import AuthRegisterRequestDTO


class RefreshTokenRequest(BaseModel):
    token: str = Field(..., description="Token")
    refresh_token: str = Field(..., description="Refresh token")


class VerifyTokenRequest(BaseModel):
    token: str = Field(..., description="Token")

class AuthLoginRequest(BaseModel):
    nickname: str = Field(... ,description="nickname or email")
    password: str

class AuthRegisterRequest(AuthRegisterRequestDTO): ...