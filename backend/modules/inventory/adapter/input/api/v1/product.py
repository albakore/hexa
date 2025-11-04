"""
Product API Router
Define los endpoints REST para la gestión de productos
"""
from typing import Optional
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Query, HTTPException, status
from pydantic import BaseModel, Field
from decimal import Decimal

from modules.container import ModuleContainer
from modules.inventory.application.service.product import ProductService
from modules.inventory.domain.entity.product import Product


# ==================== DTOs / Request Models ====================

class ProductCreateRequest(BaseModel):
    """DTO para crear un producto"""
    sku: str = Field(..., max_length=100, description="SKU único del producto")
    name: str = Field(..., max_length=255, description="Nombre del producto")
    description: Optional[str] = Field(None, description="Descripción detallada")
    category: Optional[str] = Field(None, max_length=100)
    barcode: Optional[str] = Field(None, max_length=100)
    cost_price: Decimal = Field(Decimal("0.00"), ge=0)
    sale_price: Decimal = Field(Decimal("0.00"), ge=0)
    quantity_on_hand: int = Field(0, ge=0)
    reorder_point: int = Field(10, ge=0)
    reorder_quantity: int = Field(50, ge=0)
    unit_of_measure: str = Field("unit", max_length=50)
    is_stockable: bool = Field(True)


class ProductUpdateRequest(BaseModel):
    """DTO para actualizar un producto"""
    id: int
    sku: Optional[str] = Field(None, max_length=100)
    name: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    category: Optional[str] = Field(None, max_length=100)
    barcode: Optional[str] = Field(None, max_length=100)
    cost_price: Optional[Decimal] = Field(None, ge=0)
    sale_price: Optional[Decimal] = Field(None, ge=0)
    reorder_point: Optional[int] = Field(None, ge=0)
    reorder_quantity: Optional[int] = Field(None, ge=0)
    unit_of_measure: Optional[str] = Field(None, max_length=50)
    is_active: Optional[bool] = None
    is_stockable: Optional[bool] = None


class StockAdjustmentRequest(BaseModel):
    """DTO para ajustes de stock"""
    product_id: int
    quantity: int = Field(..., description="Cantidad a ajustar (puede ser negativa)")
    is_reservation: bool = Field(False, description="Si es reserva o stock real")


class StockReservationRequest(BaseModel):
    """DTO para reservas de stock"""
    product_id: int
    quantity: int = Field(..., gt=0, description="Cantidad a reservar")


# ==================== API Router ====================

product_router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


@product_router.get("", response_model=list[Product])
@inject
async def get_all_products(
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    active_only: bool = Query(default=True),
    service: ProductService = Depends(Provide[ModuleContainer.inventory.product_service])
):
    """
    Obtiene todos los productos con paginación

    - **limit**: Número máximo de productos a retornar (1-100)
    - **offset**: Número de productos a saltar
    - **active_only**: Si es True, solo retorna productos activos
    """
    return await service.get_all_products(limit, offset, active_only)


@product_router.get("/search", response_model=list[Product])
@inject
async def search_products(
    q: str = Query(..., min_length=1, description="Término de búsqueda"),
    limit: int = Query(default=50, ge=1, le=100),
    service: ProductService = Depends(Provide[ModuleContainer.inventory.product_service])
):
    """
    Busca productos por nombre, SKU, descripción o código de barras

    - **q**: Término de búsqueda
    - **limit**: Número máximo de resultados
    """
    return await service.search_products(q, limit)


@product_router.get("/low-stock", response_model=list[Product])
@inject
async def get_low_stock_products(
    service: ProductService = Depends(Provide[ModuleContainer.inventory.product_service])
):
    """
    Obtiene productos con stock bajo (quantity_on_hand <= reorder_point)

    Útil para generar alertas y órdenes de compra automáticas
    """
    return await service.get_low_stock_products()


@product_router.get("/{product_id}", response_model=Product)
@inject
async def get_product_by_id(
    product_id: int,
    service: ProductService = Depends(Provide[ModuleContainer.inventory.product_service])
):
    """
    Obtiene un producto por su ID

    - **product_id**: ID del producto
    """
    try:
        return await service.get_product_by_id(product_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@product_router.get("/sku/{sku}", response_model=Product)
@inject
async def get_product_by_sku(
    sku: str,
    service: ProductService = Depends(Provide[ModuleContainer.inventory.product_service])
):
    """
    Obtiene un producto por su SKU

    - **sku**: SKU del producto
    """
    try:
        return await service.get_product_by_sku(sku)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@product_router.post("", response_model=Product, status_code=status.HTTP_201_CREATED)
@inject
async def create_product(
    request: ProductCreateRequest,
    service: ProductService = Depends(Provide[ModuleContainer.inventory.product_service])
):
    """
    Crea un nuevo producto

    El SKU debe ser único en el sistema
    """
    try:
        product = Product(**request.model_dump())
        return await service.create_product(product)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@product_router.put("/{product_id}", response_model=Product)
@inject
async def update_product(
    product_id: int,
    request: ProductUpdateRequest,
    service: ProductService = Depends(Provide[ModuleContainer.inventory.product_service])
):
    """
    Actualiza un producto existente

    Solo se actualizan los campos proporcionados (no nulos)
    """
    try:
        # Obtener el producto existente
        existing_product = await service.get_product_by_id(product_id)

        # Actualizar solo los campos proporcionados
        update_data = request.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            if value is not None:
                setattr(existing_product, field, value)

        return await service.update_product(existing_product)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@product_router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def delete_product(
    product_id: int,
    service: ProductService = Depends(Provide[ModuleContainer.inventory.product_service])
):
    """
    Elimina un producto (borrado lógico)

    El producto se marca como inactivo pero permanece en la base de datos
    """
    try:
        await service.delete_product(product_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


# ==================== Stock Management Endpoints ====================

@product_router.post("/stock/adjust", response_model=Product)
@inject
async def adjust_stock(
    request: StockAdjustmentRequest,
    service: ProductService = Depends(Provide[ModuleContainer.inventory.product_service])
):
    """
    Ajusta el stock de un producto

    Permite incrementar o decrementar el stock (quantity puede ser negativa)
    """
    try:
        return await service.adjust_stock(
            request.product_id,
            request.quantity,
            request.is_reservation
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@product_router.post("/stock/receive", response_model=Product)
@inject
async def receive_stock(
    product_id: int = Query(..., description="ID del producto"),
    quantity: int = Query(..., gt=0, description="Cantidad a recibir"),
    service: ProductService = Depends(Provide[ModuleContainer.inventory.product_service])
):
    """
    Recibe stock (aumenta quantity_on_hand)

    Útil para registrar recepciones de inventario
    """
    try:
        return await service.receive_stock(product_id, quantity)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@product_router.post("/stock/ship", response_model=Product)
@inject
async def ship_stock(
    product_id: int = Query(..., description="ID del producto"),
    quantity: int = Query(..., gt=0, description="Cantidad a enviar"),
    service: ProductService = Depends(Provide[ModuleContainer.inventory.product_service])
):
    """
    Envía stock (disminuye quantity_on_hand)

    Útil para registrar salidas de inventario
    """
    try:
        return await service.ship_stock(product_id, quantity)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@product_router.post("/stock/reserve", response_model=Product)
@inject
async def reserve_stock(
    request: StockReservationRequest,
    service: ProductService = Depends(Provide[ModuleContainer.inventory.product_service])
):
    """
    Reserva stock para un pedido

    Incrementa quantity_reserved y verifica que haya stock disponible
    """
    try:
        return await service.reserve_stock(request.product_id, request.quantity)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@product_router.post("/stock/release", response_model=Product)
@inject
async def release_reservation(
    product_id: int = Query(..., description="ID del producto"),
    quantity: int = Query(..., gt=0, description="Cantidad a liberar"),
    service: ProductService = Depends(Provide[ModuleContainer.inventory.product_service])
):
    """
    Libera una reserva de stock

    Decrementa quantity_reserved
    """
    try:
        return await service.release_reservation(product_id, quantity)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


# ==================== Export Router ====================

# IMPORTANTE: Exportar el router con el nombre 'router'
# El sistema de auto-descubrimiento busca este nombre
router = product_router
