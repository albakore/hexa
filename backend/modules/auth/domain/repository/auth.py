from abc import ABC, abstractmethod
import uuid

from modules.user.application.dto import LoginResponseDTO
from modules.auth.domain.entity import RecoverPassword


class AuthRepository(ABC):
	@abstractmethod
	async def create_user_session(self, login_response_dto: LoginResponseDTO): ...

	@abstractmethod
	async def get_user_session(self, user_uuid: str) -> LoginResponseDTO | None: ...

	@abstractmethod
	async def revoque_user_session(
		self, login_response_dto: LoginResponseDTO
	) -> None: ...

	@abstractmethod
	async def get_user_permissions(self, user_uuid: str): ...

	@abstractmethod
	async def delete_user_session(self, user_uuid: str): ...

	@abstractmethod
	async def create_recovery_password_request(
		self, recovery_request: RecoverPassword
	) -> RecoverPassword: ...

	@abstractmethod
	async def get_active_recovery_request(
		self, user_uuid: uuid.UUID
	) -> RecoverPassword | None: ...

	@abstractmethod
	async def mark_recovery_as_completed(self, recovery_id: uuid.UUID) -> None: ...
