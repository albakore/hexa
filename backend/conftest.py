"""
Configuración global de pytest para todos los tests del proyecto.

Este archivo contiene fixtures compartidos que están disponibles para todos los tests.
"""

import uuid
from typing import AsyncGenerator, Generator
from unittest.mock import AsyncMock, MagicMock

import pytest
from faker import Faker
from sqlalchemy.ext.asyncio import AsyncSession

from core.db.session import (
	reset_session_context,
	session,
	set_session_context,
)

# Instancia global de Faker para generar datos de prueba
faker = Faker()


# ============================================================================
# SESSION FIXTURES
# ============================================================================


@pytest.fixture(scope="function")
def session_context() -> Generator[str, None, None]:
	"""
	Fixture que crea un contexto de sesión único para cada test.

	El contexto se establece antes del test y se resetea después.
	Scope: function - Se crea un nuevo contexto para cada test.

	Yields:
	    str: UUID del contexto de sesión

	Example:
	    @pytest.mark.asyncio
	    async def test_something(session_context):
	        # El contexto ya está establecido
	        # Puedes usar session() directamente
	        async with session() as s:
	            ...
	"""
	session_uuid = str(uuid.uuid4())
	context = set_session_context(session_uuid)
	yield session_uuid
	reset_session_context(context)


@pytest.fixture(scope="function")
async def db_session(session_context: str) -> AsyncGenerator[AsyncSession, None]:
	"""
	Fixture que proporciona una sesión de base de datos con transacción.

	La sesión se crea con el contexto establecido y se cierra automáticamente.
	Todos los cambios se revierten al final del test (rollback).

	Scope: function - Nueva sesión para cada test.

	Yields:
	    AsyncSession: Sesión de base de datos lista para usar

	Example:
	    @pytest.mark.asyncio
	    async def test_repository(db_session):
	        user = User(name="Test")
	        db_session.add(user)
	        await db_session.commit()
	        # Al finalizar el test, se hace rollback automático
	"""
	async with session() as s:
		async with s.begin():
			yield s
			# Rollback automático al finalizar el test
			await s.rollback()


# ============================================================================
# FAKER FIXTURES
# ============================================================================


@pytest.fixture(scope="session")
def fake() -> Faker:
	"""
	Fixture que proporciona una instancia de Faker para generar datos de prueba.

	Scope: session - La misma instancia se reutiliza en todos los tests.

	Returns:
	    Faker: Instancia de Faker

	Example:
	    def test_user_creation(fake):
	        name = fake.name()
	        email = fake.email()
	        user = User(name=name, email=email)
	"""
	return faker


# ============================================================================
# MOCK FIXTURES
# ============================================================================


@pytest.fixture
def mock_repository() -> MagicMock:
	"""
	Fixture que proporciona un mock genérico de repositorio.

	Returns:
	    MagicMock: Mock de repositorio con métodos comunes

	Example:
	    def test_service(mock_repository):
	        mock_repository.get_by_id.return_value = User(id=1)
	        service = UserService(mock_repository)
	        result = service.get_user(1)
	"""
	mock = MagicMock()
	return mock


@pytest.fixture
def mock_async_repository() -> AsyncMock:
	"""
	Fixture que proporciona un mock asíncrono de repositorio.

	Returns:
	    AsyncMock: Mock asíncrono de repositorio

	Example:
	    @pytest.mark.asyncio
	    async def test_service(mock_async_repository):
	        mock_async_repository.get_by_id.return_value = User(id=1)
	        service = UserService(mock_async_repository)
	        result = await service.get_user(1)
	"""
	mock = AsyncMock()
	return mock


# ============================================================================
# TEST DATA FACTORIES
# ============================================================================


@pytest.fixture
def random_email(fake: Faker) -> str:
	"""Genera un email aleatorio único."""
	return fake.unique.email()


@pytest.fixture
def random_name(fake: Faker) -> str:
	"""Genera un nombre aleatorio."""
	return fake.name()


@pytest.fixture
def random_text(fake: Faker) -> str:
	"""Genera un texto aleatorio."""
	return fake.text()


@pytest.fixture
def random_uuid() -> str:
	"""Genera un UUID aleatorio como string."""
	return str(uuid.uuid4())


@pytest.fixture
def random_int(fake: Faker) -> int:
	"""Genera un entero aleatorio entre 1 y 10000."""
	return fake.random_int(min=1, max=10000)


# ============================================================================
# PYTEST CONFIGURATION
# ============================================================================


def pytest_configure(config):
	"""
	Hook de pytest que se ejecuta al inicio de la sesión de testing.

	Configura marcadores personalizados y otras opciones.
	"""
	# Registrar marcadores personalizados
	config.addinivalue_line(
		"markers", "unit: marca un test como test unitario (sin DB)"
	)
	config.addinivalue_line(
		"markers", "integration: marca un test como test de integración (con DB)"
	)
	config.addinivalue_line("markers", "e2e: marca un test como test end-to-end")
	config.addinivalue_line("markers", "slow: marca un test como lento")


def pytest_collection_modifyitems(config, items):
	"""
	Hook de pytest que se ejecuta después de recolectar los tests.

	Agrega marcadores automáticamente basándose en el nombre del test.
	"""
	for item in items:
		# Marcar tests que usan db_session como integration
		if "db_session" in item.fixturenames:
			item.add_marker(pytest.mark.integration)

		# Marcar tests que usan mocks como unit
		if any(
			fixture in item.fixturenames
			for fixture in ["mock_repository", "mock_async_repository"]
		):
			item.add_marker(pytest.mark.unit)
