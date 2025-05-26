
from app.user.domain.entity.user import User
from app.user.domain.repository.user import UserRepository


class UserRepositoryAdapter(UserRepository):

	def __init__(self, repository: UserRepository):
		self.repository = repository

	def get_user_list(self, limit: int, page: int) -> list[User]:
		return self.repository.get_user_list(limit, page)

	def get_user_by_id(self, user_id: int) -> User | None:
		return self.repository.get_user_by_id(user_id)

	def get_user_by_email(self, user_email: str) -> User | None:
		return self.repository.get_user_by_email(user_email)

	def save(self, user: User) -> None:
		return self.repository.save(user)
