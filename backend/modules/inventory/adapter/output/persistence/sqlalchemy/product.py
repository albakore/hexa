"""
Product SQLAlchemy Repository Implementation
Implementación concreta del repositorio usando SQLAlchemy/SQLModel
"""
from typing import Optional, Sequence
from sqlmodel import select, or_
from sqlalchemy.exc import IntegrityError

from modules.inventory.domain.entity.product import Product
from modules.inventory.domain.repository.product import ProductRepository
from core.db.session import session as global_session, session_factory


class ProductSQLAlchemyRepository(ProductRepository):
    """
    Implementación del repositorio de productos usando SQLAlchemy

    Utiliza SQLModel (SQLAlchemy + Pydantic) para las operaciones de base de datos.
    """

    async def get_all(
        self,
        limit: int = 50,
        offset: int = 0,
        active_only: bool = True
    ) -> Sequence[Product]:
        """Obtiene todos los productos con paginación"""
        query = select(Product)

        if active_only:
            query = query.where(Product.is_active == True)

        query = query.offset(offset).limit(limit)
        query = query.order_by(Product.name)

        async with session_factory() as session:
            result = await session.execute(query)

        return result.scalars().all()

    async def get_by_id(self, product_id: int) -> Optional[Product]:
        """Obtiene un producto por su ID"""
        stmt = select(Product).where(Product.id == product_id)

        async with session_factory() as session:
            result = await session.execute(stmt)

        return result.scalars().one_or_none()

    async def get_by_sku(self, sku: str) -> Optional[Product]:
        """Obtiene un producto por su SKU"""
        stmt = select(Product).where(Product.sku == sku)

        async with session_factory() as session:
            result = await session.execute(stmt)

        return result.scalars().one_or_none()

    async def search(
        self,
        query: str,
        limit: int = 50
    ) -> Sequence[Product]:
        """
        Busca productos por nombre, SKU o descripción

        Realiza búsqueda case-insensitive usando LIKE
        """
        search_pattern = f"%{query}%"

        stmt = select(Product).where(
            or_(
                Product.name.ilike(search_pattern),
                Product.sku.ilike(search_pattern),
                Product.description.ilike(search_pattern),
                Product.barcode.ilike(search_pattern)
            )
        ).where(
            Product.is_active == True
        ).limit(limit).order_by(Product.name)

        async with session_factory() as session:
            result = await session.execute(stmt)

        return result.scalars().all()

    async def get_low_stock(self) -> Sequence[Product]:
        """Obtiene productos con stock bajo"""
        stmt = select(Product).where(
            Product.is_active == True,
            Product.is_stockable == True,
            Product.quantity_on_hand <= Product.reorder_point
        ).order_by(Product.quantity_on_hand)

        async with session_factory() as session:
            result = await session.execute(stmt)

        return result.scalars().all()

    async def save(self, product: Product) -> Product:
        """
        Crea o actualiza un producto

        Usa la sesión global para permitir transacciones
        """
        try:
            global_session.add(product)
            await global_session.flush()
            await global_session.refresh(product)
            return product
        except IntegrityError as e:
            await global_session.rollback()
            raise ValueError(f"Error al guardar producto: {str(e)}")

    async def delete(self, product: Product) -> None:
        """
        Elimina un producto

        Implementa borrado lógico marcando is_active = False
        o borrado físico según el caso de uso
        """
        # Opción 1: Borrado lógico (recomendado)
        product.is_active = False
        global_session.add(product)
        await global_session.flush()

        # Opción 2: Borrado físico (descomentar si es necesario)
        # await global_session.delete(product)
        # await global_session.flush()

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
            is_reservation: Si es True, actualiza quantity_reserved
        """
        product = await self.get_by_id(product_id)

        if product is None:
            return None

        if is_reservation:
            product.quantity_reserved += quantity_delta
            # No permitir reservas negativas
            if product.quantity_reserved < 0:
                product.quantity_reserved = 0
        else:
            product.quantity_on_hand += quantity_delta
            # No permitir stock negativo
            if product.quantity_on_hand < 0:
                product.quantity_on_hand = 0

        return await self.save(product)
