from abc import ABC, abstractmethod


class AuthUseCase(ABC):

	@abstractmethod
	def login(self, *, email: str, password: str): ...