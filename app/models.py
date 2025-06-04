from sqlmodel import SQLModel
from sqlalchemy import Engine

from app.user.domain.entity import *
from app.rbac.domain.entity import *

def create_tables(engine : Engine):
	"""
	Crea todas las tablas en la base de datos de forma asíncrona
	"""
	SQLModel.metadata.create_all(engine)

def drop_tables(engine : Engine):
	"""
	Elimina todas las tablas de la base de datos de forma asíncrona
	"""
	SQLModel.metadata.drop_all(engine)