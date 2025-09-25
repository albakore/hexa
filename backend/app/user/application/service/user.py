from typing import List, Sequence
from app.user.domain.command import CreateUserCommand
from app.user.domain.entity.user import User
from app.user.domain.repository.user import UserRepository
from app.user.domain.usecase.user import UserUseCaseFactory


class UserService:
	def __init__(self, repository: UserRepository):
		self.repository = repository
		self.usecase = UserUseCaseFactory(repository)

	async def get_user_list(self, limit: int, page: int) -> list[User]:
		return await self.usecase.get_user_list(limit, page)

	async def get_user_by_id(self, user_id: int) -> User | None:
		return await self.usecase.get_user_by_id(user_id)

	async def get_user_by_uuid(self, user_uuid: str) -> User | None:
		return await self.usecase.get_user_by_uuid(user_uuid)

	async def get_all_user_with_roles(
		self, role_id_list: List[int]
	) -> List[User] | Sequence[User]:
		return await self.usecase.get_all_user_with_roles(role_id_list)

	async def create_user(self, *, command: CreateUserCommand) -> User | None:
		return await self.usecase.create_user(command)

	async def asign_role_to_user(self, user_uuid: str, role_id: int) -> User:
		return await self.usecase.assign_role_to_user(user_uuid, role_id)
