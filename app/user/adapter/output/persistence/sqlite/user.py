from app.user.domain.entity.user import User
from app.user.domain.repository.user import UserRepository


class UserSQLiteRepository(UserRepository):
	
	def get_user_list(self) -> list[User]:
		raise NotImplementedError

	def get_user_by_id(self, user_id: int) -> User | None:
		raise NotImplementedError

	def get_user_by_email(self, user_email: str) -> User | None:
		raise NotImplementedError

	def save(self, user: User) -> None:
		raise NotImplementedError
