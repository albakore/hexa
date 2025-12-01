from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Form

from modules.auth.application.service.auth import AuthService
from modules.auth.container import AuthContainer
from modules.auth.adapter.input.api.v1.request import (
	AuthCompleteRecoveryPasswordRequest,
	AuthLoginRequest,
	AuthPasswordResetRequest,
	AuthRecoveryPasswordRequest,
	AuthRegisterRequest,
	RefreshTokenRequest,
	VerifyTokenRequest,
)
from modules.auth.adapter.input.api.v1.response import (
	AuthCompleteRecoveryPasswordResponse,
	AuthPasswordResetResponse,
	AuthRecoveryPasswordResponse,
	RefreshTokenResponse,
)
from modules.auth.application.usecase.jwt import JwtUseCase


auth_router = APIRouter()


@auth_router.post(
	"/refresh",
	response_model=RefreshTokenResponse,
)
@inject
async def refresh_token(
	request: RefreshTokenRequest,
	usecase: JwtUseCase = Depends(Provide[AuthContainer.jwt_service]),
):
	token = await usecase.create_refresh_token(refresh_token=request.refresh_token)
	return token


@auth_router.post("/verify")
@inject
async def verify_token(
	request: VerifyTokenRequest,
	usecase: JwtUseCase = Depends(Provide[AuthContainer.jwt_service]),
):
	decoded_token = await usecase.verify_token(token=request.token)
	return decoded_token


@auth_router.post("/login")
@inject
async def login(
	request: AuthLoginRequest = Form(),
	usecase: AuthService = Depends(Provide[AuthContainer.service]),
):
	data = await usecase.login(request.nickname, request.password)
	return data


@auth_router.post("/register")
@inject
async def register(
	request: AuthRegisterRequest = Form(),
	usecase: AuthService = Depends(Provide[AuthContainer.service]),
):
	data = await usecase.register(registration_data=request)
	return data


@auth_router.post("/password_reset")
@inject
async def password_reset(
	request: AuthPasswordResetRequest = Form(),
	usecase: AuthService = Depends(Provide[AuthContainer.service]),
):
	await usecase.password_reset(
		request.id.hex, request.initial_password, request.new_password
	)
	return AuthPasswordResetResponse()


@auth_router.post("/recovery_password", response_model=AuthRecoveryPasswordResponse)
@inject
async def recovery_password(
	request: AuthRecoveryPasswordRequest = Form(),
	usecase: AuthService = Depends(Provide[AuthContainer.service]),
):
	"""
	Endpoint para solicitar recuperación de contraseña.

	Envía un email al usuario con una contraseña temporal.
	"""
	await usecase.recovery_password(request.email_or_nickname)
	return AuthRecoveryPasswordResponse()


@auth_router.post(
	"/complete_recovery_password", response_model=AuthCompleteRecoveryPasswordResponse
)
@inject
async def complete_recovery_password(
	request: AuthCompleteRecoveryPasswordRequest = Form(),
	usecase: AuthService = Depends(Provide[AuthContainer.service]),
):
	"""
	Endpoint para completar la recuperación de contraseña.

	Valida la contraseña temporal recibida por email contra el registro
	de RecoverPassword y establece la nueva contraseña del usuario.
	"""
	await usecase.complete_recovery_password(
		request.email_or_nickname, request.temporary_password, request.new_password
	)
	return AuthCompleteRecoveryPasswordResponse()


@auth_router.post("/error_intencionado")
async def error_intencionado():
	raise ValueError("Error intencionado")
