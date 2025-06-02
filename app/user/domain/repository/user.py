from abc import ABC, abstractmethod

from app.user.domain.entity.user import User


class UserRepository(ABC):

	@abstractmethod
	async def get_user_list(self, limit : int, page : int) -> list[User]: ...

	@abstractmethod
	async def get_user_by_id(self,user_id : int) -> User | None: ...

	@abstractmethod
	async def get_user_by_email(self,user_email : str) -> User | None: ...

	@abstractmethod
	async def save(self, user: User) -> User | None: ...

	@abstractmethod
	async def delete(self, user: User) -> User | None: ...