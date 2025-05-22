
from app.user.domain.entity.user import User
from app.user.domain.repository.user import UserRepository
from app.user.domain.usecase.user import UserUseCase


class UserService(UserUseCase):

	def __init__(self, repository : UserRepository):
		self.repository = repository

	def get_user_list(self) -> list[User]:
		raise NotImplementedError

	def get_user_by_id(self) -> User | None:
		raise NotImplementedError

	def get_user_by_email(self) -> User | None:
		raise NotImplementedError

	def is_active(self) -> bool:
		raise NotImplementedError

	def is_owner(self) -> bool:
		raise NotImplementedError
