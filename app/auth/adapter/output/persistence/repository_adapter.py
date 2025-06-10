
from app.auth.domain.entity.auth import AuthRepository


class AuthRepositoryAdapter(AuthRepository):

	def __init__(self, repository : AuthRepository):
		self.repository = repository
	async def create_user_session():
		raise NotImplementedError

	async def get_user_session():
		raise NotImplementedError

	async def get_user_permissions():
		raise NotImplementedError

	async def delete_user_session():
		raise NotImplementedError

		