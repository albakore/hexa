#!/usr/bin/env python3
"""
Script para generar automáticamente la estructura de tests para módulos.

Uso:
    python generate_tests.py <module_name>

Ejemplo:
    python generate_tests.py provider
    python generate_tests.py user
"""

import sys
import os
from pathlib import Path
from typing import List


def create_conftest(module_name: str, module_path: Path) -> str:
	"""Genera el contenido del conftest.py para un módulo."""

	return f'''"""
Fixtures específicos para los tests del módulo {module_name}.
"""

from datetime import date
from typing import AsyncGenerator
from unittest.mock import AsyncMock

import pytest
from faker import Faker

# TODO: Importar entidades del módulo
# from modules.{module_name}.domain.entity.your_entity import YourEntity
# from modules.{module_name}.domain.repository.your_repository import YourRepository

faker = Faker()


# ============================================================================
# ENTITY FACTORIES
# ============================================================================

# TODO: Crear fixtures de datos de ejemplo
# @pytest.fixture
# def sample_entity_data(fake: Faker) -> dict:
#     """Crea datos de ejemplo para una entidad."""
#     return {{
#         "name": fake.name(),
#         "email": fake.email(),
#         # ...
#     }}


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
#     from modules.{module_name}.domain.repository.your_repository import YourRepository
#     return AsyncMock(spec=YourRepository)


# ============================================================================
# SERVICE FIXTURES
# ============================================================================

# TODO: Crear fixtures de servicios
# @pytest.fixture
# def your_service(mock_your_repository: AsyncMock):
#     """Servicio con repositorio mockeado."""
#     from modules.{module_name}.application.service.your_service import YourService
#     return YourService(your_repository=mock_your_repository)
'''


def create_repository_test(module_name: str) -> str:
	"""Genera plantilla de tests para repositorios."""

	return f'''"""
Tests para los repositorios del módulo {module_name}.

Estos son tests de integración que verifican la interacción con la base de datos.
"""

import pytest

# TODO: Importar entidades y repositorios
# from modules.{module_name}.domain.entity.your_entity import YourEntity
# from modules.{module_name}.adapter.output.persistence.your_adapter import YourRepositoryAdapter


@pytest.mark.integration
@pytest.mark.asyncio
class TestYourRepository:
    """Suite de tests para YourRepository"""

    async def test_save_entity(
        self,
        db_session,
        # sample_entity: YourEntity,  # TODO: Descomentar y usar tu entidad
    ):
        """
        Test: Guardar una entidad en la base de datos.

        Given: Una entidad válida
        When: Se guarda en el repositorio
        Then: La entidad se guarda correctamente y se le asigna un ID
        """
        # TODO: Implementar test
        pytest.skip("Test pendiente de implementar")

        # Arrange
        # repository = YourRepositoryAdapter()
        # assert sample_entity.id is None

        # Act
        # saved_entity = await repository.save(sample_entity)

        # Assert
        # assert saved_entity.id is not None
        # assert saved_entity.name == sample_entity.name

    async def test_get_by_id(
        self,
        db_session,
    ):
        """
        Test: Obtener una entidad por ID.

        Given: Una entidad guardada en la base de datos
        When: Se busca por su ID
        Then: Se retorna la entidad correcta
        """
        # TODO: Implementar test
        pytest.skip("Test pendiente de implementar")

    async def test_get_by_id_not_found(
        self,
        db_session,
    ):
        """
        Test: Buscar una entidad que no existe.

        Given: Un ID que no existe en la base de datos
        When: Se busca la entidad
        Then: Se retorna None
        """
        # TODO: Implementar test
        pytest.skip("Test pendiente de implementar")

    async def test_get_list(
        self,
        db_session,
    ):
        """
        Test: Obtener lista paginada de entidades.

        Given: Varias entidades en la base de datos
        When: Se solicita una lista con límite y página
        Then: Se retorna la lista correcta
        """
        # TODO: Implementar test
        pytest.skip("Test pendiente de implementar")

    async def test_update_entity(
        self,
        db_session,
    ):
        """
        Test: Actualizar una entidad existente.

        Given: Una entidad guardada
        When: Se modifican sus campos y se guarda nuevamente
        Then: Los cambios se persisten correctamente
        """
        # TODO: Implementar test
        pytest.skip("Test pendiente de implementar")

    async def test_delete_entity(
        self,
        db_session,
    ):
        """
        Test: Eliminar una entidad.

        Given: Una entidad guardada
        When: Se elimina
        Then: Ya no se puede recuperar
        """
        # TODO: Implementar test
        pytest.skip("Test pendiente de implementar")
'''


def create_usecase_test(module_name: str) -> str:
	"""Genera plantilla de tests para casos de uso."""

	return f'''"""
Tests para los casos de uso del módulo {module_name}.

Estos son tests unitarios que verifican la lógica de negocio usando mocks.
"""

import pytest
from unittest.mock import AsyncMock

# TODO: Importar casos de uso
# from modules.{module_name}.domain.usecase.your_usecase import YourUseCase


@pytest.mark.unit
@pytest.mark.asyncio
class TestYourUseCase:
    """Tests para el caso de uso YourUseCase"""

    async def test_usecase_success(
        self,
        # mock_your_repository: AsyncMock,  # TODO: Descomentar
    ):
        """
        Test: Caso de uso exitoso.

        Given: Un repositorio que retorna datos válidos
        When: Se ejecuta el caso de uso
        Then: Se retorna el resultado correcto
        """
        # TODO: Implementar test
        pytest.skip("Test pendiente de implementar")

        # Arrange
        # mock_your_repository.get_by_id.return_value = expected_value
        # usecase = YourUseCase(mock_your_repository)

        # Act
        # result = await usecase(id=123)

        # Assert
        # assert result == expected_value
        # mock_your_repository.get_by_id.assert_called_once_with(123)

    async def test_usecase_not_found(
        self,
        # mock_your_repository: AsyncMock,  # TODO: Descomentar
    ):
        """
        Test: Caso de uso cuando no se encuentra el recurso.

        Given: Un repositorio que retorna None
        When: Se ejecuta el caso de uso
        Then: Se retorna None o se lanza excepción
        """
        # TODO: Implementar test
        pytest.skip("Test pendiente de implementar")
'''


def create_service_test(module_name: str) -> str:
	"""Genera plantilla de tests para servicios."""

	return f'''"""
Tests para los servicios del módulo {module_name}.

Estos son tests unitarios que verifican la lógica del servicio usando mocks.
"""

import pytest
from unittest.mock import AsyncMock

# TODO: Importar servicio
# from modules.{module_name}.application.service.your_service import YourService


@pytest.mark.unit
@pytest.mark.asyncio
class TestYourService:
    """Suite de tests para YourService"""

    async def test_service_method_success(
        self,
        # your_service: YourService,  # TODO: Descomentar
        # mock_your_repository: AsyncMock,  # TODO: Descomentar
    ):
        """
        Test: Método del servicio exitoso.

        Given: Un servicio con repositorio mockeado
        When: Se ejecuta el método
        Then: Se retorna el resultado correcto
        """
        # TODO: Implementar test
        pytest.skip("Test pendiente de implementar")

        # Arrange
        # mock_your_repository.get_by_id.return_value = expected_value

        # Act
        # result = await your_service.get_by_id(123)

        # Assert
        # assert result == expected_value

    async def test_service_method_not_found(
        self,
        # your_service: YourService,  # TODO: Descomentar
        # mock_your_repository: AsyncMock,  # TODO: Descomentar
    ):
        """
        Test: Método del servicio cuando no encuentra recurso.

        Given: Un repositorio que retorna None
        When: Se ejecuta el método
        Then: Se lanza la excepción apropiada
        """
        # TODO: Implementar test
        pytest.skip("Test pendiente de implementar")


@pytest.mark.integration
@pytest.mark.asyncio
class TestYourServiceIntegration:
    """Tests de integración para el servicio con repositorio real"""

    async def test_full_flow(
        self,
        db_session,
    ):
        """
        Test de integración: Flujo completo con repositorio real.

        Given: Un servicio con repositorio real
        When: Se ejecuta un flujo completo
        Then: Todo funciona correctamente
        """
        # TODO: Implementar test de integración
        pytest.skip("Test pendiente de implementar")
'''


def create_init_file() -> str:
	"""Genera __init__.py vacío."""
	return '"""Tests para el módulo."""\n'


def generate_tests_for_module(module_name: str):
	"""Genera estructura de tests para un módulo."""

	# Definir paths
	backend_path = Path(__file__).parent
	module_path = backend_path / "modules" / module_name
	test_path = module_path / "test"

	# Verificar que el módulo existe
	if not module_path.exists():
		print(f"❌ Error: El módulo '{module_name}' no existe en modules/")
		sys.exit(1)

	# Crear directorio de tests
	test_path.mkdir(exist_ok=True)
	print(f"✅ Creado directorio: {test_path.relative_to(backend_path)}")

	# Crear archivos
	files = {
		"__init__.py": create_init_file(),
		"conftest.py": create_conftest(module_name, module_path),
		f"test_{module_name}_repository.py": create_repository_test(module_name),
		f"test_{module_name}_usecase.py": create_usecase_test(module_name),
		f"test_{module_name}_service.py": create_service_test(module_name),
	}

	for filename, content in files.items():
		filepath = test_path / filename

		# No sobreescribir archivos existentes
		if filepath.exists():
			print(f"⚠️  Ya existe: {filepath.relative_to(backend_path)} (omitido)")
			continue

		filepath.write_text(content)
		print(f"✅ Creado: {filepath.relative_to(backend_path)}")

	print(f"\n🎉 Estructura de tests generada para el módulo '{module_name}'")
	print(f"\n📝 Próximos pasos:")
	print(f"   1. Editar {test_path.relative_to(backend_path)}/conftest.py")
	print(f"   2. Implementar los tests marcados con TODO")
	print(f"   3. Ejecutar: ./run_tests.sh module {module_name}")


def main():
	if len(sys.argv) < 2:
		print("❌ Error: Debes especificar el nombre del módulo")
		print(f"\nUso: python {sys.argv[0]} <module_name>")
		print(f"\nEjemplo: python {sys.argv[0]} provider")
		print(f"\nMódulos disponibles:")

		backend_path = Path(__file__).parent
		modules_path = backend_path / "modules"

		if modules_path.exists():
			for module_dir in sorted(modules_path.iterdir()):
				if module_dir.is_dir() and not module_dir.name.startswith("_"):
					module_file = module_dir / "module.py"
					if module_file.exists():
						print(f"   - {module_dir.name}")

		sys.exit(1)

	module_name = sys.argv[1]
	generate_tests_for_module(module_name)


if __name__ == "__main__":
	main()
