"""
Product Application Service
Servicio de aplicación que orquesta las operaciones de productos
"""
from dataclasses import dataclass
from typing import Optional, Sequence

from modules.inventory.domain.entity.product import Product
from modules.inventory.domain.repository.product import ProductRepository


@dataclass
class ProductService:
    """
    Servicio de aplicación para productos

    Orquesta las operaciones de negocio relacionadas con productos,
    delegando al repositorio para la persistencia.
    """
    product_repository: ProductRepository

    async def get_all_products(
        self,
        limit: int = 50,
        offset: int = 0,
        active_only: bool = True
    ) -> Sequence[Product]:
        """Obtiene todos los productos con paginación"""
        return await self.product_repository.get_all(limit, offset, active_only)

    async def get_product_by_id(self, product_id: int) -> Optional[Product]:
        """Obtiene un producto por su ID"""
        product = await self.product_repository.get_by_id(product_id)
        if not product:
            raise ValueError(f"Producto con ID {product_id} no encontrado")
        return product

    async def get_product_by_sku(self, sku: str) -> Optional[Product]:
        """Obtiene un producto por su SKU"""
        product = await self.product_repository.get_by_sku(sku)
        if not product:
            raise ValueError(f"Producto con SKU {sku} no encontrado")
        return product

    async def search_products(
        self,
        query: str,
        limit: int = 50
    ) -> Sequence[Product]:
        """Busca productos por nombre, SKU o descripción"""
        return await self.product_repository.search(query, limit)

    async def get_low_stock_products(self) -> Sequence[Product]:
        """Obtiene productos con stock bajo"""
        return await self.product_repository.get_low_stock()

    async def create_product(self, product: Product) -> Product:
        """
        Crea un nuevo producto

        Valida que el SKU no exista antes de crear
        """
        # Verificar que el SKU no exista
        existing = await self.product_repository.get_by_sku(product.sku)
        if existing:
            raise ValueError(f"Ya existe un producto con SKU {product.sku}")

        return await self.product_repository.save(product)

    async def update_product(self, product: Product) -> Product:
        """Actualiza un producto existente"""
        # Verificar que el producto exista
        existing = await self.product_repository.get_by_id(product.id)
        if not existing:
            raise ValueError(f"Producto con ID {product.id} no encontrado")

        return await self.product_repository.save(product)

    async def delete_product(self, product_id: int) -> None:
        """Elimina un producto"""
        product = await self.product_repository.get_by_id(product_id)
        if not product:
            raise ValueError(f"Producto con ID {product_id} no encontrado")

        await self.product_repository.delete(product)

    async def adjust_stock(
        self,
        product_id: int,
        quantity_delta: int,
        is_reservation: bool = False
    ) -> Product:
        """
        Ajusta el stock de un producto

        Args:
            product_id: ID del producto
            quantity_delta: Cambio en la cantidad (positivo para aumentar, negativo para disminuir)
            is_reservation: Si es True, ajusta reservas en lugar de stock disponible

        Returns:
            Producto actualizado

        Raises:
            ValueError: Si el producto no existe o el ajuste resulta en stock negativo
        """
        product = await self.product_repository.update_stock(
            product_id,
            quantity_delta,
            is_reservation
        )

        if not product:
            raise ValueError(f"Producto con ID {product_id} no encontrado")

        return product

    async def receive_stock(
        self,
        product_id: int,
        quantity: int
    ) -> Product:
        """
        Recibe stock (aumenta quantity_on_hand)

        Método de conveniencia para operaciones de recepción de inventario
        """
        if quantity <= 0:
            raise ValueError("La cantidad debe ser positiva")

        return await self.adjust_stock(product_id, quantity, is_reservation=False)

    async def ship_stock(
        self,
        product_id: int,
        quantity: int
    ) -> Product:
        """
        Envía stock (disminuye quantity_on_hand)

        Método de conveniencia para operaciones de envío
        """
        if quantity <= 0:
            raise ValueError("La cantidad debe ser positiva")

        return await self.adjust_stock(product_id, -quantity, is_reservation=False)

    async def reserve_stock(
        self,
        product_id: int,
        quantity: int
    ) -> Product:
        """
        Reserva stock para un pedido

        Aumenta quantity_reserved
        """
        if quantity <= 0:
            raise ValueError("La cantidad debe ser positiva")

        # Verificar que haya suficiente stock disponible
        product = await self.product_repository.get_by_id(product_id)
        if not product:
            raise ValueError(f"Producto con ID {product_id} no encontrado")

        if product.quantity_available < quantity:
            raise ValueError(
                f"Stock insuficiente. Disponible: {product.quantity_available}, "
                f"Requerido: {quantity}"
            )

        return await self.adjust_stock(product_id, quantity, is_reservation=True)

    async def release_reservation(
        self,
        product_id: int,
        quantity: int
    ) -> Product:
        """
        Libera una reserva de stock

        Disminuye quantity_reserved
        """
        if quantity <= 0:
            raise ValueError("La cantidad debe ser positiva")

        return await self.adjust_stock(product_id, -quantity, is_reservation=True)
