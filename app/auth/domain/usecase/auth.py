from abc import ABC, abstractmethod

from app.auth.application.dto import AuthRegisterRequestDTO
from app.user.application.dto import LoginResponseDTO
from app.user.domain.entity import User


class AuthUseCase(ABC):

	@abstractmethod
	def login(self, *, email: str, password: str) -> LoginResponseDTO | Exception: ...

	@abstractmethod
	def register(self, *, registration_data : AuthRegisterRequestDTO) -> User | None | Exception : ...