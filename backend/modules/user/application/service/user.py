from typing import List, Sequence

from modules.user.domain.command import CreateUserCommand
from modules.user.domain.entity.user import User
from modules.user.domain.repository.user import UserRepository
from modules.user.domain.usecase.user import UserUseCaseFactory


class UserService:
	def __init__(self, repository: UserRepository):
		self.repository = repository
		self.usecase = UserUseCaseFactory(repository)

	async def get_user_list(
		self, limit: int | None = None, page: int = 0
	) -> list[User] | Sequence[User]:
		return await self.usecase.get_user_list(limit, page)

	async def get_user_by_id(self, user_id: int) -> User | None:
		return await self.usecase.get_user_by_id(user_id)

	async def get_user_by_uuid(self, user_uuid: str) -> User | None:
		return await self.usecase.get_user_by_uuid(user_uuid)

	async def get_all_user_with_roles(
		self, role_id_list: List[int]
	) -> List[User] | Sequence[User]:
		return await self.usecase.get_all_user_with_roles(role_id_list)

	async def create_user(self, command: CreateUserCommand) -> User | None:
		return await self.usecase.create_user(command)

	async def asign_role_to_user(self, user_uuid: str, role_id: int) -> User:
		return await self.usecase.assign_role_to_user(user_uuid, role_id)

	async def get_user_by_email_or_nickname(
		self, email: str, nickname: str, with_role: bool = False
	) -> User | None:
		"""Obtiene usuario por email o nickname (usado por auth)"""
		return await self.repository.get_user_by_email_or_nickname(
			email=email, nickname=nickname, with_role=with_role
		)

	async def save_user(self, user: User) -> User:
		"""Guarda un usuario (usado por auth para register)"""
		return await self.repository.save(user)

	async def set_user_password(self, user: User, hashed_password: str) -> User:
		"""Establece la contraseña de un usuario (usado por auth para reset)"""
		return await self.repository.set_user_password(user, hashed_password)
