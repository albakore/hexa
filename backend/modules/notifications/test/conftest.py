"""
Fixtures específicos para los tests del módulo notifications.
"""

from datetime import date
from typing import AsyncGenerator
from unittest.mock import AsyncMock

import pytest
from faker import Faker

# TODO: Importar entidades del módulo
# from modules.notifications.domain.entity.your_entity import YourEntity
# from modules.notifications.domain.repository.your_repository import YourRepository

faker = Faker()


# ============================================================================
# ENTITY FACTORIES
# ============================================================================

# TODO: Crear fixtures de datos de ejemplo
# @pytest.fixture
# def sample_entity_data(fake: Faker) -> dict:
#     """Crea datos de ejemplo para una entidad."""
#     return {
#         "name": fake.name(),
#         "email": fake.email(),
#         # ...
#     }


# @pytest.fixture
# def sample_entity(sample_entity_data: dict) -> YourEntity:
#     """Crea una instancia de entidad con datos de ejemplo."""
#     return YourEntity(**sample_entity_data)


# ============================================================================
# REPOSITORY FIXTURES
# ============================================================================

# TODO: Crear mocks de repositorios
# @pytest.fixture
# def mock_your_repository() -> AsyncMock:
#     """Mock del repositorio."""
#     from modules.notifications.domain.repository.your_repository import YourRepository
#     return AsyncMock(spec=YourRepository)


# ============================================================================
# SERVICE FIXTURES
# ============================================================================

# TODO: Crear fixtures de servicios
# @pytest.fixture
# def your_service(mock_your_repository: AsyncMock):
#     """Servicio con repositorio mockeado."""
#     from modules.notifications.application.service.your_service import YourService
#     return YourService(your_repository=mock_your_repository)
