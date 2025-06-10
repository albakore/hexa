from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Form, Response

from app.auth.adapter.input.api.v1.request import (
    AuthLoginRequest,
    AuthPasswordResetRequest,
    AuthRegisterRequest,
    RefreshTokenRequest,
    VerifyTokenRequest,
)
from app.auth.adapter.input.api.v1.response import AuthPasswordResetResponse, RefreshTokenResponse
from app.auth.domain.usecase.auth import AuthUseCase
from app.auth.domain.usecase.jwt import JwtUseCase
from app.container import MainContainer

auth_router = APIRouter()


@auth_router.post(
    "/refresh",
    response_model=RefreshTokenResponse,
)
@inject
async def refresh_token(
    request: RefreshTokenRequest,
    usecase: JwtUseCase = Depends(Provide[MainContainer.jwt_service]),
):
    token = await usecase.create_refresh_token(
        token=request.token, refresh_token=request.refresh_token
    )
    return {"token": token.token, "refresh_token": token.refresh_token}


@auth_router.post("/verify")
@inject
async def verify_token(
    request: VerifyTokenRequest,
    usecase: JwtUseCase = Depends(Provide[MainContainer.jwt_service]),
):
    await usecase.verify_token(token=request.token)
    return Response(status_code=200)


@auth_router.post("/login")
@inject
async def login(
    request: AuthLoginRequest = Form(),
    usecase: AuthUseCase = Depends(Provide[MainContainer.auth.service]),
):
    data = await usecase.login(
        request.nickname,
        request.password
    )
    return data


@auth_router.post("/register")
@inject
async def register(
    request: AuthRegisterRequest = Form(),
    usecase: AuthUseCase = Depends(Provide[MainContainer.auth.service]),
):
    data = await usecase.register(
        registration_data=request
    )
    return data

@auth_router.post("/password_reset")
@inject
async def password_reset(
    request: AuthPasswordResetRequest = Form(),
    usecase: AuthUseCase = Depends(Provide[MainContainer.auth.service]),
):
    await usecase.password_reset(
        request.id.hex,
        request.initial_password,
        request.new_password
    )
    return AuthPasswordResetResponse()