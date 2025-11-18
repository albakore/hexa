from abc import ABC, abstractmethod
from typing import List, Sequence

from modules.user.domain.entity.user import User


class UserRepository(ABC):
	@abstractmethod
	async def get_user_list(
		self, limit: int | None, page: int
	) -> List[User] | Sequence[User]: ...

	@abstractmethod
	async def get_user_by_id(
		self, user_id: int, with_role: bool = False
	) -> User | None: ...

	@abstractmethod
	async def get_user_by_uuid(
		self, user_uuid: str, with_role: bool = False
	) -> User | None: ...

	@abstractmethod
	async def get_all_user_with_roles(
		self, role_id_list: List[int]
	) -> List[User] | Sequence[User]: ...

	@abstractmethod
	async def get_user_by_email(self, user_email: str) -> User | None: ...

	@abstractmethod
	async def get_user_by_email_or_nickname(
		self, email: str, nickname: str, with_role: bool = False
	) -> User | None: ...

	@abstractmethod
	async def set_user_password(self, user: User, password: str) -> None: ...

	@abstractmethod
	async def save(self, user: User) -> User: ...

	@abstractmethod
	async def delete(self, user: User) -> None: ...
