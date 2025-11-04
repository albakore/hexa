"""
Product Entity
Entidad de dominio que representa un producto en el inventario
"""
from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field
from decimal import Decimal


class Product(SQLModel, table=True):
    """
    Producto en el inventario

    Representa un artículo en el inventario con sus características
    y niveles de stock.
    """
    __tablename__ = "product"

    # Identificación
    id: Optional[int] = Field(default=None, primary_key=True)
    sku: str = Field(unique=True, index=True, max_length=100)
    name: str = Field(max_length=255)
    description: Optional[str] = Field(default=None)

    # Categorización
    category: Optional[str] = Field(default=None, max_length=100)
    barcode: Optional[str] = Field(default=None, max_length=100, unique=True)

    # Precios
    cost_price: Decimal = Field(
        default=Decimal("0.00"),
        max_digits=10,
        decimal_places=2,
        description="Precio de costo"
    )
    sale_price: Decimal = Field(
        default=Decimal("0.00"),
        max_digits=10,
        decimal_places=2,
        description="Precio de venta"
    )

    # Stock
    quantity_on_hand: int = Field(
        default=0,
        description="Cantidad disponible en inventario"
    )
    quantity_reserved: int = Field(
        default=0,
        description="Cantidad reservada para pedidos"
    )
    reorder_point: int = Field(
        default=10,
        description="Punto de reorden (alerta de stock bajo)"
    )
    reorder_quantity: int = Field(
        default=50,
        description="Cantidad a ordenar cuando se alcance el punto de reorden"
    )

    # Unidades y medidas
    unit_of_measure: str = Field(
        default="unit",
        max_length=50,
        description="Unidad de medida (ej: unit, kg, liter)"
    )

    # Estado
    is_active: bool = Field(default=True, description="Producto activo")
    is_stockable: bool = Field(
        default=True,
        description="Si el producto maneja inventario"
    )

    # Auditoría
    created_at: Optional[datetime] = Field(
        default_factory=datetime.utcnow,
        nullable=False
    )
    updated_at: Optional[datetime] = Field(
        default_factory=datetime.utcnow,
        nullable=False
    )

    # Propiedades calculadas
    @property
    def quantity_available(self) -> int:
        """Cantidad disponible para venta (en mano - reservado)"""
        return max(0, self.quantity_on_hand - self.quantity_reserved)

    @property
    def is_low_stock(self) -> bool:
        """Verifica si el stock está bajo"""
        return self.quantity_on_hand <= self.reorder_point

    @property
    def stock_value(self) -> Decimal:
        """Valor total del stock (cantidad * precio de costo)"""
        return Decimal(self.quantity_on_hand) * self.cost_price

    def __repr__(self) -> str:
        return f"<Product(id={self.id}, sku='{self.sku}', name='{self.name}', stock={self.quantity_on_hand})>"
