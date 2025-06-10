from abc import ABC, abstractmethod

from app.user.domain.command import CreateUserCommand
from app.user.domain.entity.user import User

class UserUseCase(ABC):

	@abstractmethod
	def get_user_list(self,) -> list[User]: ...

	@abstractmethod
	def get_user_by_id(self,) -> User | None: ...

	@abstractmethod
	def get_user_by_uuid(self,user_uuid: str) -> User | None: ...

	@abstractmethod
	def get_user_by_email(self,) -> User | None: ...

	@abstractmethod
	def create_user(self,command: CreateUserCommand) -> User | None: ...

	@abstractmethod
	def is_active(self,) -> bool: ...

	@abstractmethod
	def is_admin(self,user_id) -> bool: ...
	
	@abstractmethod
	def is_owner(self,) -> bool: ...