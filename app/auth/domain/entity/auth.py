
from abc import ABC, abstractmethod


class AuthRepository(ABC):
	
	@abstractmethod
	async def create_user_session(self): ...

	@abstractmethod
	async def get_user_session(self): ...

	@abstractmethod
	async def revoque_user_session(self): ...

	@abstractmethod
	async def get_user_permissions(self): ...

	@abstractmethod
	async def delete_user_session(self): ...

