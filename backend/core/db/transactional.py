from functools import wraps
from typing import Callable, TypeVar, Awaitable, ParamSpec
from core.db import session

P = ParamSpec("P")
R = TypeVar("R")


class Transactional:
	def __call__(self, func: Callable[P, Awaitable[R]]) -> Callable[P, Awaitable[R]]:
		@wraps(func)
		async def _transactional(*args, **kwargs):
			try:
				result = await func(*args, **kwargs)
				await session.commit()
			except Exception as e:
				await session.rollback()
				raise e

			return result

		return _transactional
