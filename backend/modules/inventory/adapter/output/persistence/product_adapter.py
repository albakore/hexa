"""
Product Repository Adapter
Adaptador que delega al repositorio concreto
"""
from typing import Optional, Sequence
from modules.inventory.domain.entity.product import Product
from modules.inventory.domain.repository.product import ProductRepository


class ProductRepositoryAdapter(ProductRepository):
    """
    Adaptador del repositorio de productos

    Sigue el patrón Adapter para desacoplar la interfaz del dominio
    de la implementación concreta.
    """

    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository

    async def get_all(
        self,
        limit: int = 50,
        offset: int = 0,
        active_only: bool = True
    ) -> Sequence[Product]:
        return await self.product_repository.get_all(limit, offset, active_only)

    async def get_by_id(self, product_id: int) -> Optional[Product]:
        return await self.product_repository.get_by_id(product_id)

    async def get_by_sku(self, sku: str) -> Optional[Product]:
        return await self.product_repository.get_by_sku(sku)

    async def search(
        self,
        query: str,
        limit: int = 50
    ) -> Sequence[Product]:
        return await self.product_repository.search(query, limit)

    async def get_low_stock(self) -> Sequence[Product]:
        return await self.product_repository.get_low_stock()

    async def save(self, product: Product) -> Product:
        return await self.product_repository.save(product)

    async def delete(self, product: Product) -> None:
        return await self.product_repository.delete(product)

    async def update_stock(
        self,
        product_id: int,
        quantity_delta: int,
        is_reservation: bool = False
    ) -> Optional[Product]:
        return await self.product_repository.update_stock(
            product_id,
            quantity_delta,
            is_reservation
        )
