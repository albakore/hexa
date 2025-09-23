from typing import List, Sequence
from uuid import UUID
from app.user.domain.entity.user import User
from app.user.domain.repository.user import UserRepository


class UserRepositoryAdapter(UserRepository):
	def __init__(self, repository: UserRepository):
		self.repository = repository

	async def get_user_list(self, limit: int, page: int) -> List[User] | Sequence[User]:
		return await self.repository.get_user_list(limit, page)

	async def get_user_by_id(
		self, user_id: int, with_role: bool = False
	) -> User | None:
		return await self.repository.get_user_by_id(user_id, with_role)

	async def get_user_by_uuid(
		self, user_uuid: str, with_role: bool = False
	) -> User | None:
		return await self.repository.get_user_by_uuid(user_uuid, with_role)

	async def get_user_by_email(self, user_email: str) -> User | None:
		return await self.repository.get_user_by_email(user_email)

	async def save(self, user: User) -> User:
		return await self.repository.save(user)

	async def delete(self, user: User) -> None:
		return await self.repository.delete(user)

	async def get_user_by_email_or_nickname(
		self, email: str, nickname: str, with_role: bool = False
	) -> User | None:
		return await self.repository.get_user_by_email_or_nickname(
			email, nickname, with_role
		)

	async def set_user_password(self, user: User, password: str) -> None:
		return await self.repository.set_user_password(user, password)

	async def get_all_user_with_roles(
		self, role_id_list: List[int]
	) -> List[User] | Sequence[User]:
		return await self.repository.get_all_user_with_roles(role_id_list)
