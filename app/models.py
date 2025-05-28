from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import AsyncEngine

from app.user.domain.entity import *
from app.role.domain.entity import *

async def create_tables(async_engine : AsyncEngine):
	"""
	Crea todas las tablas en la base de datos de forma asíncrona
	"""
	async with async_engine.begin() as conn:
		await conn.run_sync(SQLModel.metadata.create_all)

async def drop_tables(async_engine : AsyncEngine):
	"""
	Elimina todas las tablas de la base de datos de forma asíncrona
	"""
	async with async_engine.begin() as conn:
		await conn.run_sync(SQLModel.metadata.drop_all)