from abc import ABC, abstractmethod

from app.user.domain.entity.user import User


class UserRepository(ABC):

	@abstractmethod
	def get_user_list(self,) -> list[User]: ...

	@abstractmethod
	def get_user_by_id(self,user_id : int) -> User | None: ...

	@abstractmethod
	def get_user_by_email(self,user_email : str) -> User | None: ...

	@abstractmethod
	def save(self, user: User) -> None: ...