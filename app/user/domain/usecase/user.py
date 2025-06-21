from abc import ABC, abstractmethod

from app.user.domain.command import CreateUserCommand
from app.user.domain.entity.user import User
from app.rbac.domain.entity.role import Role

class UserUseCase(ABC):

	@abstractmethod
	async def get_user_list(self,) -> list[User]: ...

	@abstractmethod
	async def get_user_by_id(self,user_id:int, with_role:bool = False) -> User | None: ...

	@abstractmethod
	async def get_user_by_uuid(self,user_uuid: str, with_role:bool = False) -> User | None: ...

	@abstractmethod
	async def get_user_by_email(self,) -> User | None: ...

	@abstractmethod
	async def create_user(self,command: CreateUserCommand) -> User | None: ...

	@abstractmethod
	async def is_active(self,) -> bool: ...

	@abstractmethod
	async def is_admin(self,user_id) -> bool: ...
	
	@abstractmethod
	async def is_owner(self,) -> bool: ...

	@abstractmethod
	async def asign_role_to_user(self, user: str, role: int) -> User: ...