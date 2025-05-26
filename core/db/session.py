from core.config.settings import env

from sqlmodel import Session, create_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine

async_engine = create_async_engine(env.ENV)
sync_engine = create_engine(env.ENV)


async def get_session():
	with Session(sync_engine) as session:
		try:
			yield session
		except Exception as e:
			session.rollback()
			raise e
		finally:
			session.close()


async def get_async_session():
	async with AsyncSession(async_engine) as session:
		try:
			yield session
		except Exception as e:
			await session.rollback()
			raise e
		finally:
			await session.close()
