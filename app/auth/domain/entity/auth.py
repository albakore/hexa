
from abc import ABC, abstractmethod


class AuthRepository(ABC):
	
	@abstractmethod
	async def create_user_session(): ...

	@abstractmethod
	async def get_user_session(): ...

	@abstractmethod
	async def get_user_permissions(): ...

	@abstractmethod
	async def delete_user_session(): ...

