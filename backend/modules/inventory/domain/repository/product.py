"""
Product Repository Interface
Define el contrato para la persistencia de productos
"""
from abc import ABC, abstractmethod
from typing import Optional, Sequence
from modules.inventory.domain.entity.product import Product


class ProductRepository(ABC):
    """
    Repositorio abstracto para la entidad Product

    Define las operaciones de persistencia sin implementar
    los detalles de cómo se almacenan los datos.
    """

    @abstractmethod
    async def get_all(
        self,
        limit: int = 50,
        offset: int = 0,
        active_only: bool = True
    ) -> Sequence[Product]:
        """
        Obtiene todos los productos con paginación

        Args:
            limit: Número máximo de productos a retornar
            offset: Número de productos a saltar
            active_only: Si es True, solo retorna productos activos

        Returns:
            Lista de productos
        """
        ...

    @abstractmethod
    async def get_by_id(self, product_id: int) -> Optional[Product]:
        """
        Obtiene un producto por su ID

        Args:
            product_id: ID del producto

        Returns:
            Producto si existe, None si no existe
        """
        ...

    @abstractmethod
    async def get_by_sku(self, sku: str) -> Optional[Product]:
        """
        Obtiene un producto por su SKU

        Args:
            sku: SKU del producto

        Returns:
            Producto si existe, None si no existe
        """
        ...

    @abstractmethod
    async def search(
        self,
        query: str,
        limit: int = 50
    ) -> Sequence[Product]:
        """
        Busca productos por nombre, SKU o descripción

        Args:
            query: Término de búsqueda
            limit: Número máximo de resultados

        Returns:
            Lista de productos que coinciden con la búsqueda
        """
        ...

    @abstractmethod
    async def get_low_stock(self) -> Sequence[Product]:
        """
        Obtiene productos con stock bajo (quantity_on_hand <= reorder_point)

        Returns:
            Lista de productos con stock bajo
        """
        ...

    @abstractmethod
    async def save(self, product: Product) -> Product:
        """
        Crea o actualiza un producto

        Args:
            product: Producto a guardar

        Returns:
            Producto guardado con ID asignado
        """
        ...

    @abstractmethod
    async def delete(self, product: Product) -> None:
        """
        Elimina un producto

        Args:
            product: Producto a eliminar
        """
        ...

    @abstractmethod
    async def update_stock(
        self,
        product_id: int,
        quantity_delta: int,
        is_reservation: bool = False
    ) -> Optional[Product]:
        """
        Actualiza el stock de un producto

        Args:
            product_id: ID del producto
            quantity_delta: Cambio en la cantidad (puede ser negativo)
            is_reservation: Si es True, actualiza quantity_reserved en lugar de quantity_on_hand

        Returns:
            Producto actualizado o None si no existe
        """
        ...
