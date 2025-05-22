from abc import ABC, abstractmethod

from app.user.domain.entity.user import User

class UserUseCase(ABC):

	@abstractmethod
	def get_user_list(self,) -> list[User]: ...

	@abstractmethod
	def get_user_by_id(self,) -> User | None: ...

	@abstractmethod
	def get_user_by_email(self,) -> User | None: ...

	@abstractmethod
	def is_active(self,) -> bool: ...
	
	@abstractmethod
	def is_owner(self,) -> bool: ...