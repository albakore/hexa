from contextlib import asynccontextmanager
from contextvars import ContextVar, Token
from enum import Enum
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import Delete, Insert, Update

from core.config.settings import env

session_context: ContextVar[str] = ContextVar("session_context")


def get_session_context() -> str:
    #print(f"GET contexto de sesion: {session_context.get()}")
    return session_context.get()


def set_session_context(session_id: str) -> Token:
    #print(f"SET contexto de sesion: {session_id}")
    return session_context.set(session_id)


def reset_session_context(context: Token) -> None:
    session_context.reset(context)
    #print(f"RESET contexto de sesion: {context}")


class EngineType(Enum):
    WRITER = "writer"
    READER = "reader"


engines = {
    EngineType.WRITER: create_async_engine(
        env.DATABASE_URL,
        pool_recycle=3600,
        pool_size=20,        # Aumentado de 5 a 20
        max_overflow=20,     # Aumentado de 10 a 20
        pool_timeout=60,     # Aumentado de 30 a 60 segundos
        pool_pre_ping=True,  # Verificar conexiones antes de usar
    ),
    EngineType.READER: create_async_engine(
        env.DATABASE_URL,
        pool_recycle=3600,
        pool_size=20,        # Aumentado de 5 a 20
        max_overflow=20,     # Aumentado de 10 a 20
        pool_timeout=60,     # Aumentado de 30 a 60 segundos
        pool_pre_ping=True,  # Verificar conexiones antes de usar
    ),
}


class RoutingSession(Session):
    def get_bind(self, mapper=None, clause=None, **kw):
        if self._flushing or isinstance(clause, (Update, Delete, Insert)):
            return engines[EngineType.WRITER].sync_engine
        else:
            return engines[EngineType.READER].sync_engine


_async_session_factory = async_sessionmaker(
    class_=AsyncSession,
    sync_session_class=RoutingSession,
    expire_on_commit=False,
    autoflush=True
)
session = async_scoped_session(
    session_factory=_async_session_factory,
    scopefunc=get_session_context,
)


@asynccontextmanager
async def session_factory() -> AsyncGenerator[AsyncSession, None]:
    _session = async_sessionmaker(
        class_=AsyncSession,
        sync_session_class=RoutingSession,
        expire_on_commit=False,
    )()
    try:
        yield _session
    finally:
        await _session.close()
