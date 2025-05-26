from typing import List
from app.user.domain.entity.user import User
from app.user.domain.repository.user import UserRepository
from sqlmodel import select
from core.db.session import session as global_session, session_factory

class UserSQLiteRepository(UserRepository):
	async def get_user_list(self, limit: int = 12, page: int = 0) -> List[User]:
		query = select(User)

		async with session_factory() as session:
			result = await session.execute(query)
		
		return list(result.scalars().all())
			


	async def get_user_by_id(self, user_id: int) -> User | None:
		raise NotImplementedError

	async def get_user_by_email(self, user_email: str) -> User | None:
		raise NotImplementedError

	async def save(self, user: User) -> None:
		raise NotImplementedError
