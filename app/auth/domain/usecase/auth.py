from abc import ABC, abstractmethod
from app.user.domain.entity import User


class AuthUseCase(ABC):

	@abstractmethod
	async def login(self,email: str, password: str): ...

	@abstractmethod
	async def register(self,registration_data) -> User | None | Exception : ...