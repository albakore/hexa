
from abc import ABC, abstractmethod


class AuthRepository(ABC):
	
	@abstractmethod
	def create_user_session(): ...

	@abstractmethod
	def get_user_session(): ...

	@abstractmethod
	def get_user_permissions(): ...

	@abstractmethod
	def delete_user_session(): ...

