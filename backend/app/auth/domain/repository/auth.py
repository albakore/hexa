
from abc import ABC, abstractmethod

from app.user.application.dto import LoginResponseDTO
from app.user.application.dto.user import UserLoginResponseDTO


class AuthRepository(ABC):
	
	@abstractmethod
	async def create_user_session(self, login_response_dto : LoginResponseDTO): ...

	@abstractmethod
	async def get_user_session(self, user_uuid : str) -> LoginResponseDTO | None: ...

	@abstractmethod
	async def revoque_user_session(self, login_response_dto : LoginResponseDTO) -> None: ...

	@abstractmethod
	async def get_user_permissions(self, user_uuid : str): ...

	@abstractmethod
	async def delete_user_session(self, user_uuid : str): ...

