from typing import List, Sequence
from app.user.domain.entity.user import User
from app.user.domain.repository.user import UserRepository
from sqlmodel import or_, select
from core.db.session import session as global_session, session_factory

class UserSQLAlchemyRepository(UserRepository):
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

	async def delete(self, user: User) -> None:
		await global_session.delete(user)
		await global_session.flush()

	async def get_user_by_email_or_nickname(
		self,
		email: str,
		nickname: str,
	) -> User | None:
		async with session_factory() as read_session:
			stmt = await read_session.execute(
				select(User).where(or_(User.email == email, User.nickname == nickname)),
			)
			return stmt.scalars().first()


			
		
