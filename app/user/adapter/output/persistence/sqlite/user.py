from typing import List, Sequence
from app.user.domain.entity.user import User
from app.user.domain.repository.user import UserRepository
from sqlmodel import select
from core.db.session import session as global_session, session_factory

class UserSQLiteRepository(UserRepository):
	async def get_user_list(self, limit: int = 12, page: int = 0) -> List[User] | Sequence[User]:
		query = select(User)
		query = query.slice(page,limit)

		async with session_factory() as session:
			result = await session.execute(query)
		
		return result.scalars().all()
			


	async def get_user_by_id(self, user_id: int) -> User | None:
		async with session_factory() as session:
			instance = await session.get(User,int(user_id))
		return instance


	async def get_user_by_email(self, user_email: str) -> User | None:
		async with session_factory() as session:
			query = select(User).where(User.email == str(user_email))
			result = await session.execute(query)
			
		return result.scalars().one_or_none()

	async def save(self, user: User) -> User | None:
		global_session.add(user)
		await global_session.flush()
		return user
			
		
