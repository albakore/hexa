from fastapi import APIRouter, Form, Depends
from shared.dependencies import get_auth_service, get_jwt_service, get_user_service

from modules.auth.adapter.input.api.v1.request import (
	AuthLoginRequest,
	AuthPasswordResetRequest,
	AuthRegisterRequest,
	RefreshTokenRequest,
	VerifyTokenRequest,
)
from modules.auth.adapter.input.api.v1.response import (
	AuthPasswordResetResponse,
	RefreshTokenResponse,
)

auth_router = APIRouter()


@auth_router.post(
	"/refresh",
	response_model=RefreshTokenResponse,
)
async def refresh_token(
	request: RefreshTokenRequest,
	jwt_service = Depends(get_jwt_service),
):
	token = await jwt_service.create_refresh_token(refresh_token=request.refresh_token)
	return token


@auth_router.post("/verify")
async def verify_token(
	request: VerifyTokenRequest,
	jwt_service = Depends(get_jwt_service),
):
	decoded_token = await jwt_service.verify_token(token=request.token)
	return decoded_token


@auth_router.post("/login")
async def login(
	request: AuthLoginRequest = Form(),
	auth_service = Depends(get_auth_service),
):
	data = await auth_service.login(request.nickname, request.password)
	return data


@auth_router.post("/register")
async def register(
	request: AuthRegisterRequest = Form(),
	user_service = Depends(get_user_service),
):
	user_data = {
		"email": request.email,
		"nickname": request.nickname,
		"password": request.password,
		"initial_password": request.initial_password
	}
	data = await user_service.create_user(user_data)
	return data


@auth_router.post("/password_reset")
async def password_reset(
	request: AuthPasswordResetRequest = Form(),
	auth_service = Depends(get_auth_service),
):
	await auth_service.password_reset(
		request.id.hex, request.initial_password, request.new_password
	)
	return AuthPasswordResetResponse()
