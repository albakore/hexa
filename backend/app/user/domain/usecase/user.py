from abc import ABC, abstractmethod
from typing import List, Sequence

from app.user.domain.command import CreateUserCommand
from app.user.domain.entity.user import User
from app.rbac.domain.entity.role import Role
from dataclasses import dataclass
from app.user.domain.repository.user import UserRepository
from core.db import Transactional

from app.user.domain.exception import UserNotFoundException


@dataclass
class GetUserListUseCase:
	user_repository: UserRepository

	async def __call__(self, limit: int = 20, page: int = 0) -> list[User]:
		return await self.user_repository.get_user_list(limit, page)


@dataclass
class GetUserByIdUseCase:
	user_repository: UserRepository

	async def __call__(self, user_id: int, with_role: bool = False) -> User | None:
		return await self.user_repository.get_user_by_id(user_id, with_role)


@dataclass
class GetUserByUuidUseCase:
	user_repository: UserRepository

	async def __call__(self, user_uuid: str, with_role: bool = False) -> User | None:
		return await self.user_repository.get_user_by_uuid(user_uuid, with_role)


@dataclass
class GetAllUserWithRoleUseCase:
	user_repository: UserRepository

	async def __call__(self, role_list: List[Role]) -> List[User] | Sequence[User]:
		return await self.user_repository.get_all_user_with_roles(role_list)


@dataclass
class GetUserByEmailUseCase:
	user_repository: UserRepository

	async def __call__(self, email: str) -> User | None:
		return await self.user_repository.get_user_by_email(email)


@dataclass
class CreateUserUseCase:
	user_repository: UserRepository

	@Transactional()
	async def __call__(self, command: CreateUserCommand) -> User | None:
		user = User.model_validate(command)
		new_user = await self.user_repository.save(user=user)
		return new_user


@dataclass
class IsActiveUseCase:
	user_repository: UserRepository

	async def __call__(self, user_id: int) -> bool:
		raise NotImplementedError


@dataclass
class IsAdminUseCase:
	user_repository: UserRepository

	async def __call__(self, user_id: int) -> bool:
		raise NotImplementedError


@dataclass
class IsOwnerUseCase:
	user_repository: UserRepository

	async def __call__(self, user_id: int) -> bool:
		raise NotImplementedError


@dataclass
class AssignRoleToUserUseCase:
	user_repository: UserRepository

	@Transactional()
	async def __call__(self, user_uuid: str, role_id: int) -> User:
		user = await self.user_repository.get_user_by_uuid(user_uuid)
		if not user:
			raise UserNotFoundException
		user.fk_role = role_id
		user = await self.user_repository.save(user)
		return user


@dataclass
class UserUseCaseFactory:
	user_repository: UserRepository

	def __post_init__(self):
		self.get_user_list = GetUserListUseCase(self.user_repository)
		self.get_user_by_id = GetUserByIdUseCase(self.user_repository)
		self.get_user_by_uuid = GetUserByUuidUseCase(self.user_repository)
		self.get_all_user_with_roles = GetAllUserWithRoleUseCase(self.user_repository)
		self.get_user_by_email = GetUserByEmailUseCase(self.user_repository)
		self.create_user = CreateUserUseCase(self.user_repository)
		self.is_active = IsActiveUseCase(self.user_repository)
		self.is_admin = IsAdminUseCase(self.user_repository)
		self.is_owner = IsOwnerUseCase(self.user_repository)
		self.assign_role_to_user = AssignRoleToUserUseCase(self.user_repository)
