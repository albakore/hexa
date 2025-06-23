from datetime import datetime, timedelta

from fastapi.encoders import jsonable_encoder
import rich
from app.auth.application.dto import RefreshTokenResponseDTO
from app.auth.application.exception import AuthSessionExpiredException, DecodeTokenException
from app.auth.domain.repository.auth import AuthRepository
from app.auth.domain.usecase.jwt import JwtUseCase
from app.rbac.domain.entity import permission
from app.rbac.domain.repository import RBACRepository
from app.user.application.dto import LoginResponseDTO
from app.user.application.dto.user import UserLoginResponseDTO
from core.helpers.token import (
	TokenHelper,
	DecodeTokenException as JwtDecodeTokenException,
	ExpiredTokenException as JwtExpiredTokenException,
)


class JwtService(JwtUseCase):
	def __init__(self, auth_repository: AuthRepository, rbac_repository : RBACRepository):
		self.auth_repository = auth_repository
		self.rbac_repository = rbac_repository
		self.access_token_expiration_minutes = 15
		self.refresh_token_expiration_days = 7

	async def verify_token(self, token: str):
		try:
			return TokenHelper.decode(token=token)
		except (JwtDecodeTokenException, JwtExpiredTokenException) as e:
			raise e

	async def create_refresh_token(
		self,
		refresh_token: str,
	) -> RefreshTokenResponseDTO:
		decoded_refresh_token = TokenHelper.decode(token=refresh_token)
		
		if decoded_refresh_token.get("sub") != "refresh":
			raise DecodeTokenException

		login_response_dto = UserLoginResponseDTO.model_validate(decoded_refresh_token)

		session = await self.auth_repository.get_user_session(
			str(login_response_dto.id)
		)

		if not session:
			raise AuthSessionExpiredException
		
		if not refresh_token == session.refresh_token:
			raise Exception

		permissions = []

		if session.user.fk_role:
			role = await self.rbac_repository.get_role_by_id(session.user.fk_role)
			if role:
				permissions_of_role = await self.rbac_repository.get_all_permissions_from_role(role)
				permissions = [permission.token for permission in permissions_of_role]


		new_login_response_dto = UserLoginResponseDTO.model_validate(session.user)
		login_dump = jsonable_encoder(new_login_response_dto)
		access_token = TokenHelper.encode(login_dump, TokenHelper.get_expiration_minutes())

		login_dump["sub"] = "refresh"
		new_refresh_token = TokenHelper.encode(login_dump, TokenHelper.get_expiration_days())

		refresh_response = RefreshTokenResponseDTO(
			user=session.user, 
			permissions=permissions,
			token=access_token, 
			refresh_token=new_refresh_token
		)

		await self.auth_repository.revoque_user_session(refresh_response)

		return refresh_response
