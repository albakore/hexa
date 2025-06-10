from app.auth.domain.entity.auth import AuthRepository


class AuthRepositoryAdapter(AuthRepository):
	def __init__(self, repository: AuthRepository):
		self.repository = repository

	async def create_user_session(self):
		raise NotImplementedError

	async def get_user_session(self):
		raise NotImplementedError

	async def get_user_permissions(self):
		raise NotImplementedError

	async def delete_user_session(self):
		raise NotImplementedError

	async def revoque_user_session(self):
		raise NotImplementedError
