from app.auth.domain.entity.auth import AuthRepository


class RedisAuthRepository(AuthRepository):
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
