from abc import ABC, abstractmethod


class JwtUseCase(ABC):
	@abstractmethod
	async def verify_token(self, token: str) -> None:
		"""Verify token"""

	@abstractmethod
	async def create_refresh_token(
		self,
		refresh_token: str,
	):
		"""Create refresh token"""
