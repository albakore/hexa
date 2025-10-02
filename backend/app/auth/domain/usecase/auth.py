from abc import ABC, abstractmethod
from modules.user.domain.entity import User


class AuthUseCase(ABC):
	@abstractmethod
	async def login(self, email: str, password: str): ...

	@abstractmethod
	async def register(self, registration_data) -> User | None | Exception: ...

	@abstractmethod
	async def password_reset(
		self, user_uuid: str, initial_password: str, new_password: str
	) -> bool | Exception: ...
