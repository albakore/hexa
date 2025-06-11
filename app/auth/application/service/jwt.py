from datetime import datetime, timedelta

from fastapi.encoders import jsonable_encoder
import rich
import rich.json
from app.auth.application.dto import RefreshTokenResponseDTO
from app.auth.application.exception import AuthSessionExpiredException, DecodeTokenException
from app.auth.domain.entity.auth import AuthRepository
from app.auth.domain.usecase.jwt import JwtUseCase
from app.user.application.dto import LoginResponseDTO
from app.user.application.dto.user import UserLoginResponseDTO
from core.helpers.token import (
	TokenHelper,
	DecodeTokenException as JwtDecodeTokenException,
	ExpiredTokenException as JwtExpiredTokenException,
)


class JwtService(JwtUseCase):
	def __init__(self, auth_repository: AuthRepository):
		self.auth_repository = auth_repository
		self.access_token_expiration_minutes = 15
		self.refresh_token_expiration_days = 7

	def _get_expiration_days(self):
		datetime_now = datetime.now()
		expiration_time = datetime_now + timedelta(
			days=self.refresh_token_expiration_days
		)
		ttl_seconds = int((expiration_time - datetime_now).total_seconds())
		return ttl_seconds

	def _get_expiration_minutes(self):
		datetime_now = datetime.now()
		expiration_time = datetime_now + timedelta(
			minutes=self.access_token_expiration_minutes
		)
		ttl_seconds = int((expiration_time - datetime_now).total_seconds())
		return ttl_seconds

	async def verify_token(self, token: str) -> None:
		try:
			TokenHelper.decode(token=token)
		except (JwtDecodeTokenException, JwtExpiredTokenException):
			raise DecodeTokenException

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

		new_login_response_dto = UserLoginResponseDTO.model_validate(session.user)
		login_dump = jsonable_encoder(new_login_response_dto)
		access_token = TokenHelper.encode(login_dump, self._get_expiration_minutes())

		login_dump["sub"] = "refresh"
		new_refresh_token = TokenHelper.encode(login_dump, self._get_expiration_days())

		refresh_response = RefreshTokenResponseDTO(
			user=session.user, 
			token=access_token, 
			refresh_token=new_refresh_token
		)

		await self.auth_repository.revoque_user_session(refresh_response)

		return refresh_response
