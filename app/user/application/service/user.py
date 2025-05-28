
from app.user.domain.command import CreateUserCommand
from app.user.domain.entity.user import User
from app.user.domain.repository.user import UserRepository
from app.user.domain.usecase.user import UserUseCase
from core.db.transactional import Transactional


class UserService(UserUseCase):

	def __init__(self, repository : UserRepository):
		self.repository = repository

	async def get_user_list(self, limit: int, page:int) -> list[User]:
		data = await self.repository.get_user_list(limit,page)
		return data

	def get_user_by_id(self) -> User | None:
		raise NotImplementedError

	def get_user_by_email(self) -> User | None:
		raise NotImplementedError

	def is_active(self,user_id) -> bool:
		raise NotImplementedError

	def is_owner(self) -> bool:
		raise NotImplementedError

	def is_admin(self) -> bool:
		raise NotImplementedError
	
	@Transactional()
	async def create_user(self, *, command: CreateUserCommand) -> None:
		user = User.model_validate(command)
		await self.repository.save(user=user)

