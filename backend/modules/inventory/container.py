"""
Inventory Module Container
Configuración de inyección de dependencias para el módulo de inventario
"""
from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Singleton, Factory

from modules.inventory.adapter.output.persistence.sqlalchemy.product import (
    ProductSQLAlchemyRepository,
)
from modules.inventory.adapter.output.persistence.product_adapter import (
    ProductRepositoryAdapter,
)
from modules.inventory.application.service.product import ProductService


class InventoryContainer(DeclarativeContainer):
    """
    Contenedor de inyección de dependencias del módulo de inventario

    Configura todos los servicios, repositorios y adaptadores del módulo,
    siguiendo el patrón Dependency Injection.

    Estructura:
    1. Repositorios concretos (SQLAlchemy) - Singleton
    2. Adaptadores de repositorio - Factory
    3. Servicios de aplicación - Factory
    """

    # ==================== Repositories ====================

    # Repositorio concreto de productos (SQLAlchemy)
    product_repo = Singleton(
        ProductSQLAlchemyRepository
    )

    # ==================== Repository Adapters ====================

    # Adaptador del repositorio de productos
    product_repo_adapter = Factory(
        ProductRepositoryAdapter,
        product_repository=product_repo
    )

    # ==================== Application Services ====================

    # Servicio de productos
    product_service = Factory(
        ProductService,
        product_repository=product_repo_adapter
    )
