import uuid
from typing import List, Sequence

from sqlalchemy.orm import selectinload
from sqlmodel import col, or_, select

from core.db.session import session as global_session
from core.db.session import session_factory
from modules.user.domain.entity import User
from modules.user.domain.repository.user import UserRepository


class UserSQLAlchemyRepository(UserRepository):
	async def get_user_list(
		self, limit: int | None = None, page: int = 0
	) -> List[User] | Sequence[User]:
		query = select(User)
		if not limit and isinstance(limit, int):
			offset = page * limit
			query = query.offset(offset).limit(limit)

		async with session_factory() as session:
			result = await session.execute(query)

		return result.scalars().all()

	async def get_user_by_id(
		self, user_id: int, with_role: bool = False
	) -> User | None:
		stmt = select(User).where(User.id == int(user_id))

		if with_role:
			stmt = stmt.options(selectinload(User.role))  # type: ignore

		async with session_factory() as session:
			instance = await session.execute(stmt)
		return instance.scalars().one_or_none()

	async def get_user_by_uuid(
		self, user_uuid: str, with_role: bool = False
	) -> User | None:
		stmt = select(User).where(User.id == uuid.UUID(user_uuid))

		if with_role:
			stmt = stmt.options(selectinload(User.role))  # type: ignore

		async with session_factory() as session:
			instance = await session.execute(stmt)
		return instance.scalars().one_or_none()

	async def get_user_by_email(self, user_email: str) -> User | None:
		async with session_factory() as session:
			query = select(User).where(User.email == str(user_email))
			result = await session.execute(query)

		return result.scalars().one_or_none()

	async def save(self, user: User) -> User:
		global_session.add(user)
		await global_session.flush()
		return user

	async def delete(self, user: User) -> None:
		await global_session.delete(user)
		await global_session.flush()

	async def get_user_by_email_or_nickname(
		self, email: str, nickname: str, with_role: bool = False
	) -> User | None:
		stmt = select(User).where(or_(User.email == email, User.nickname == nickname))
		if with_role:
			stmt = stmt.options(selectinload(User.role))  # type: ignore

		async with session_factory() as session:
			instance = await session.execute(stmt)
		return instance.scalars().first()

	async def set_user_password(self, user: User, password: str) -> None:
		user.password = password
		user.requires_password_reset = False
		global_session.add(user)

	async def get_all_user_with_roles(
		self, role_id_list: List[int]
	) -> List[User] | Sequence[User]:
		query = select(User).where(col(User.fk_role).in_(role_id_list))

		async with session_factory() as session:
			instance = await session.execute(query)
		return instance.scalars().all()
