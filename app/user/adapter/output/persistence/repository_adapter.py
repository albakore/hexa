
from app.user.domain.entity.user import User
from app.user.domain.repository.user import UserRepository


class UserRepositoryAdapter(UserRepository):

	def __init__(self, repository: UserRepository):
		self.repository = repository

	async def get_user_list(self, limit: int, page: int) -> list[User]:
		return await self.repository.get_user_list(limit, page)

	async def get_user_by_id(self, user_id: int) -> User | None:
		return await self.repository.get_user_by_id(user_id)

	async def get_user_by_email(self, user_email: str) -> User | None:
		return await self.repository.get_user_by_email(user_email)

	async def save(self, user: User) -> User | None:
		return await self.repository.save(user)

	async def delete(self, user: User) -> None:
		return await self.repository.delete(user)

