from datetime import datetime, timedelta

import jwt

from core.config.settings import env
from core.exceptions import CustomException


class DecodeTokenException(CustomException):
	code = 400
	error_code = "TOKEN__DECODE_ERROR"
	message = "token decode error"


class ExpiredTokenException(CustomException):
	code = 400
	error_code = "TOKEN__EXPIRE_TOKEN"
	message = "expired token"


class TokenHelper:

	@staticmethod
	def get_expiration_days(days: int = env.JWT_REFRESH_TOKEN_EXPIRATION_DAYS):
		datetime_now = datetime.now().astimezone()
		expiration_time = datetime_now + timedelta(
			days=days
		)
		ttl_seconds = int((expiration_time - datetime_now).total_seconds())
		return ttl_seconds

	@staticmethod
	def get_expiration_minutes(minutes:int = env.JWT_ACCESS_TOKEN_EXPIRATION_MINUTES):
		datetime_now = datetime.now().astimezone()
		expiration_time = datetime_now + timedelta(
			minutes=minutes
		)
		ttl_seconds = int((expiration_time - datetime_now).total_seconds())
		return ttl_seconds

	@staticmethod
	def encode(payload: dict, expire_period: int = 60) -> str:
		token = jwt.encode(
			payload={
				**payload,
				"exp": datetime.now().astimezone() + timedelta(seconds=expire_period),
			},
			key=env.JWT_SECRET_KEY,
			algorithm=env.JWT_ALGORITHM,
		)
		return token

	@staticmethod
	def decode(token: str) -> dict:
		try:
			return jwt.decode(
				token,
				env.JWT_SECRET_KEY,
				[env.JWT_ALGORITHM],
			)
		except jwt.exceptions.DecodeError:
			raise DecodeTokenException
		except jwt.exceptions.ExpiredSignatureError:
			raise ExpiredTokenException

	@staticmethod
	def decode_expired_token(token: str) -> dict:
		try:
			return jwt.decode(
				token,
				env.JWT_SECRET_KEY,
				env.JWT_ALGORITHM,
				options={"verify_exp": False},
			)
		except jwt.exceptions.DecodeError:
			raise DecodeTokenException
