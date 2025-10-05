# Tutorial Completo: Creando un Módulo de Productos

## Introducción

En este tutorial aprenderás a crear un módulo completo desde cero siguiendo la arquitectura hexagonal del proyecto. Crearemos un módulo de **Productos** que incluirá:

- ✅ Gestión CRUD de productos
- ✅ Integración con otros módulos (usuarios, roles)
- ✅ Validaciones de negocio
- ✅ Tests unitarios e integración
- ✅ Documentación de API

## Paso 1: Análisis y Diseño

### Requisitos del Módulo

**Entidad Producto:**
- ID único
- Nombre del producto
- Descripción
- Precio
- Categoría
- Stock disponible
- Estado (activo/inactivo)
- Usuario que lo creó
- Fechas de creación y actualización

**Casos de Uso:**
- Crear producto (solo usuarios con rol "admin" o "manager")
- Listar productos (todos los usuarios autenticados)
- Buscar productos por categoría
- Actualizar producto (solo el creador o admin)
- Eliminar producto (solo admin)
- Gestionar stock

## Paso 2: Crear la Estructura

```bash
# Crear estructura del módulo
mkdir -p modules/product/{adapter/{input/api/v1,output/persistence/sqlalchemy},application/{service,dto},domain/{entity,repository}}

# Crear archivos principales
touch modules/product/{__init__.py,container.py,module.py}
touch modules/product/adapter/{__init__.py,input/__init__.py,output/__init__.py}
touch modules/product/adapter/input/api/{__init__.py,v1/__init__.py}
touch modules/product/adapter/output/persistence/{__init__.py,sqlalchemy/__init__.py}
touch modules/product/application/{__init__.py,service/__init__.py,dto/__init__.py}
touch modules/product/domain/{__init__.py,entity/__init__.py,repository/__init__.py}
```

## Paso 3: Definir el Dominio

### 3.1 Entidad de Dominio

```python
# modules/product/domain/entity/product.py
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from decimal import Decimal

@dataclass
class Product:
    """Entidad de dominio para Producto."""
    
    id: Optional[int] = None
    name: str = ""
    description: str = ""
    price: Decimal = Decimal('0.00')
    category: str = ""
    stock: int = 0
    active: bool = True
    created_by: Optional[str] = None  # User ID
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    def __post_init__(self):
        """Validaciones de dominio."""
        if self.price < 0:
            raise ValueError("Price cannot be negative")
        if self.stock < 0:
            raise ValueError("Stock cannot be negative")
        if not self.name.strip():
            raise ValueError("Product name is required")
    
    def update_stock(self, quantity: int) -> None:
        """Actualizar stock del producto."""
        new_stock = self.stock + quantity
        if new_stock < 0:
            raise ValueError("Insufficient stock")
        self.stock = new_stock
    
    def is_available(self) -> bool:
        """Verificar si el producto está disponible."""
        return self.active and self.stock > 0
```

### 3.2 Interface del Repositorio

```python
# modules/product/domain/repository/product.py
from abc import ABC, abstractmethod
from typing import List, Optional
from ..entity.product import Product

class ProductRepositoryInterface(ABC):
    """Interface para el repositorio de productos."""
    
    @abstractmethod
    async def save(self, product: Product) -> Product:
        """Guardar un producto."""
        pass
    
    @abstractmethod
    async def find_by_id(self, product_id: int) -> Optional[Product]:
        """Buscar producto por ID."""
        pass
    
    @abstractmethod
    async def find_all(self, limit: int = 10, offset: int = 0) -> List[Product]:
        """Obtener todos los productos con paginación."""
        pass
    
    @abstractmethod
    async def find_by_category(self, category: str) -> List[Product]:
        """Buscar productos por categoría."""
        pass
    
    @abstractmethod
    async def find_by_name(self, name: str) -> List[Product]:
        """Buscar productos por nombre (búsqueda parcial)."""
        pass
    
    @abstractmethod
    async def delete(self, product_id: int) -> bool:
        """Eliminar un producto."""
        pass
    
    @abstractmethod
    async def update_stock(self, product_id: int, quantity: int) -> bool:
        """Actualizar stock de un producto."""
        pass
```

## Paso 4: Capa de Aplicación

### 4.1 DTOs y Comandos

```python
# modules/product/application/dto/product.py
from pydantic import BaseModel, Field, validator
from decimal import Decimal
from typing import Optional
from datetime import datetime

class CreateProductCommand(BaseModel):
    """Comando para crear un producto."""
    name: str = Field(..., min_length=1, max_length=200)
    description: str = Field("", max_length=1000)
    price: Decimal = Field(..., gt=0, decimal_places=2)
    category: str = Field(..., min_length=1, max_length=100)
    stock: int = Field(..., ge=0)
    
    @validator('name')
    def validate_name(cls, v):
        return v.strip()
    
    @validator('category')
    def validate_category(cls, v):
        return v.strip().lower()

class UpdateProductCommand(BaseModel):
    """Comando para actualizar un producto."""
    id: int
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    price: Optional[Decimal] = Field(None, gt=0, decimal_places=2)
    category: Optional[str] = Field(None, min_length=1, max_length=100)
    stock: Optional[int] = Field(None, ge=0)
    active: Optional[bool] = None

class UpdateStockCommand(BaseModel):
    """Comando para actualizar stock."""
    product_id: int
    quantity: int  # Puede ser negativo para reducir stock

class ProductResponse(BaseModel):
    """Respuesta con datos del producto."""
    id: int
    name: str
    description: str
    price: Decimal
    category: str
    stock: int
    active: bool
    created_by: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True

class ProductListResponse(BaseModel):
    """Respuesta para lista de productos."""
    products: List[ProductResponse]
    total: int
    page: int
    limit: int
```

### 4.2 Servicio de Aplicación

```python
# modules/product/application/service/product.py
from typing import List, Optional
from datetime import datetime
from shared.interfaces.service_locator import service_locator

from ..dto.product import (
    CreateProductCommand, 
    UpdateProductCommand, 
    UpdateStockCommand,
    ProductResponse, 
    ProductListResponse
)
from ...domain.entity.product import Product
from ...domain.repository.product import ProductRepositoryInterface

class ProductService:
    """Servicio de aplicación para productos."""
    
    def __init__(self, repository: ProductRepositoryInterface):
        self.repository = repository
    
    async def create_product(self, command: CreateProductCommand, created_by: str) -> ProductResponse:
        """Crear un nuevo producto."""
        # Validar permisos
        await self._check_create_permission(created_by)
        
        # Crear entidad de dominio
        product = Product(
            name=command.name,
            description=command.description,
            price=command.price,
            category=command.category,
            stock=command.stock,
            created_by=created_by,
            created_at=datetime.utcnow()
        )
        
        # Guardar
        saved_product = await self.repository.save(product)
        return ProductResponse.from_orm(saved_product)
    
    async def get_product_by_id(self, product_id: int) -> Optional[ProductResponse]:
        """Obtener producto por ID."""
        product = await self.repository.find_by_id(product_id)
        if not product:
            return None
        return ProductResponse.from_orm(product)
    
    async def get_products(self, limit: int = 10, page: int = 0) -> ProductListResponse:
        """Obtener lista de productos con paginación."""
        offset = page * limit
        products = await self.repository.find_all(limit, offset)
        
        # Contar total (en implementación real, agregar método count al repositorio)
        total = len(products)  # Simplificado para el tutorial
        
        return ProductListResponse(
            products=[ProductResponse.from_orm(p) for p in products],
            total=total,
            page=page,
            limit=limit
        )
    
    async def search_products_by_category(self, category: str) -> List[ProductResponse]:
        """Buscar productos por categoría."""
        products = await self.repository.find_by_category(category.lower())
        return [ProductResponse.from_orm(p) for p in products]
    
    async def update_product(self, command: UpdateProductCommand, user_id: str) -> ProductResponse:
        """Actualizar un producto."""
        # Verificar que el producto existe
        existing_product = await self.repository.find_by_id(command.id)
        if not existing_product:
            raise ValueError("Product not found")
        
        # Verificar permisos
        await self._check_update_permission(user_id, existing_product.created_by)
        
        # Actualizar campos
        if command.name is not None:
            existing_product.name = command.name
        if command.description is not None:
            existing_product.description = command.description
        if command.price is not None:
            existing_product.price = command.price
        if command.category is not None:
            existing_product.category = command.category.lower()
        if command.stock is not None:
            existing_product.stock = command.stock
        if command.active is not None:
            existing_product.active = command.active
        
        existing_product.updated_at = datetime.utcnow()
        
        # Guardar
        updated_product = await self.repository.save(existing_product)
        return ProductResponse.from_orm(updated_product)
    
    async def update_stock(self, command: UpdateStockCommand) -> ProductResponse:
        """Actualizar stock de un producto."""
        product = await self.repository.find_by_id(command.product_id)
        if not product:
            raise ValueError("Product not found")
        
        # Usar método de dominio
        product.update_stock(command.quantity)
        product.updated_at = datetime.utcnow()
        
        # Guardar
        updated_product = await self.repository.save(product)
        return ProductResponse.from_orm(updated_product)
    
    async def delete_product(self, product_id: int, user_id: str) -> bool:
        """Eliminar un producto (solo admin)."""
        await self._check_delete_permission(user_id)
        return await self.repository.delete(product_id)
    
    # Métodos privados para validación de permisos
    async def _check_create_permission(self, user_id: str) -> None:
        """Verificar permisos de creación."""
        rbac_service = service_locator.get_service("rbac.role_service")
        if not rbac_service:
            raise RuntimeError("RBAC service not available")
        
        user_roles = await rbac_service.get_user_roles(user_id)
        allowed_roles = ["admin", "manager"]
        
        if not any(role in allowed_roles for role in user_roles):
            raise PermissionError("Insufficient permissions to create products")
    
    async def _check_update_permission(self, user_id: str, created_by: str) -> None:
        """Verificar permisos de actualización."""
        # El creador puede actualizar su producto
        if user_id == created_by:
            return
        
        # Los admin pueden actualizar cualquier producto
        rbac_service = service_locator.get_service("rbac.role_service")
        if rbac_service:
            user_roles = await rbac_service.get_user_roles(user_id)
            if "admin" in user_roles:
                return
        
        raise PermissionError("Insufficient permissions to update this product")
    
    async def _check_delete_permission(self, user_id: str) -> None:
        """Verificar permisos de eliminación (solo admin)."""
        rbac_service = service_locator.get_service("rbac.role_service")
        if not rbac_service:
            raise RuntimeError("RBAC service not available")
        
        user_roles = await rbac_service.get_user_roles(user_id)
        if "admin" not in user_roles:
            raise PermissionError("Only administrators can delete products")
```

## Paso 5: Adaptadores

### 5.1 Repositorio SQLAlchemy

```python
# modules/product/adapter/output/persistence/sqlalchemy/product.py
from sqlalchemy import Column, Integer, String, Numeric, Boolean, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional
from datetime import datetime

from shared.models import Base
from ....domain.entity.product import Product

class ProductModel(Base):
    """Modelo SQLAlchemy para productos."""
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, index=True)
    description = Column(Text, default="")
    price = Column(Numeric(10, 2), nullable=False)
    category = Column(String(100), nullable=False, index=True)
    stock = Column(Integer, default=0)
    active = Column(Boolean, default=True, index=True)
    created_by = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class ProductSQLAlchemyRepository:
    """Implementación SQLAlchemy del repositorio de productos."""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def save(self, product: Product) -> Product:
        """Guardar un producto."""
        if product.id:
            # Actualizar existente
            stmt = select(ProductModel).where(ProductModel.id == product.id)
            result = await self.session.execute(stmt)
            db_product = result.scalar_one_or_none()
            
            if db_product:
                db_product.name = product.name
                db_product.description = product.description
                db_product.price = product.price
                db_product.category = product.category
                db_product.stock = product.stock
                db_product.active = product.active
                db_product.updated_at = product.updated_at or datetime.utcnow()
            else:
                raise ValueError("Product not found for update")
        else:
            # Crear nuevo
            db_product = ProductModel(
                name=product.name,
                description=product.description,
                price=product.price,
                category=product.category,
                stock=product.stock,
                active=product.active,
                created_by=product.created_by,
                created_at=product.created_at or datetime.utcnow()
            )
            self.session.add(db_product)
        
        await self.session.commit()
        await self.session.refresh(db_product)
        
        return self._to_domain(db_product)
    
    async def find_by_id(self, product_id: int) -> Optional[Product]:
        """Buscar producto por ID."""
        stmt = select(ProductModel).where(ProductModel.id == product_id)
        result = await self.session.execute(stmt)
        db_product = result.scalar_one_or_none()
        
        return self._to_domain(db_product) if db_product else None
    
    async def find_all(self, limit: int = 10, offset: int = 0) -> List[Product]:
        """Obtener todos los productos."""
        stmt = select(ProductModel).offset(offset).limit(limit)
        result = await self.session.execute(stmt)
        db_products = result.scalars().all()
        
        return [self._to_domain(db_product) for db_product in db_products]
    
    async def find_by_category(self, category: str) -> List[Product]:
        """Buscar productos por categoría."""
        stmt = select(ProductModel).where(ProductModel.category == category)
        result = await self.session.execute(stmt)
        db_products = result.scalars().all()
        
        return [self._to_domain(db_product) for db_product in db_products]
    
    async def find_by_name(self, name: str) -> List[Product]:
        """Buscar productos por nombre."""
        stmt = select(ProductModel).where(ProductModel.name.ilike(f"%{name}%"))
        result = await self.session.execute(stmt)
        db_products = result.scalars().all()
        
        return [self._to_domain(db_product) for db_product in db_products]
    
    async def delete(self, product_id: int) -> bool:
        """Eliminar un producto."""
        stmt = select(ProductModel).where(ProductModel.id == product_id)
        result = await self.session.execute(stmt)
        db_product = result.scalar_one_or_none()
        
        if db_product:
            await self.session.delete(db_product)
            await self.session.commit()
            return True
        return False
    
    def _to_domain(self, db_product: ProductModel) -> Product:
        """Convertir modelo de DB a entidad de dominio."""
        return Product(
            id=db_product.id,
            name=db_product.name,
            description=db_product.description,
            price=db_product.price,
            category=db_product.category,
            stock=db_product.stock,
            active=db_product.active,
            created_by=db_product.created_by,
            created_at=db_product.created_at,
            updated_at=db_product.updated_at
        )
```

### 5.2 Adaptador de Repositorio

```python
# modules/product/adapter/output/persistence/repository_adapter.py
from typing import List, Optional
from ...domain.repository.product import ProductRepositoryInterface
from ...domain.entity.product import Product
from .sqlalchemy.product import ProductSQLAlchemyRepository

class ProductRepositoryAdapter(ProductRepositoryInterface):
    """Adaptador para el repositorio de productos."""
    
    def __init__(self, repository: ProductSQLAlchemyRepository):
        self.repository = repository
    
    async def save(self, product: Product) -> Product:
        return await self.repository.save(product)
    
    async def find_by_id(self, product_id: int) -> Optional[Product]:
        return await self.repository.find_by_id(product_id)
    
    async def find_all(self, limit: int = 10, offset: int = 0) -> List[Product]:
        return await self.repository.find_all(limit, offset)
    
    async def find_by_category(self, category: str) -> List[Product]:
        return await self.repository.find_by_category(category)
    
    async def find_by_name(self, name: str) -> List[Product]:
        return await self.repository.find_by_name(name)
    
    async def delete(self, product_id: int) -> bool:
        return await self.repository.delete(product_id)
    
    async def update_stock(self, product_id: int, quantity: int) -> bool:
        product = await self.repository.find_by_id(product_id)
        if not product:
            return False
        
        product.update_stock(quantity)
        await self.repository.save(product)
        return True
```

### 5.3 Controlador API

```python
# modules/product/adapter/input/api/v1/product.py
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, Query, status
from typing import List

from modules.product.container import ProductContainer
from modules.product.application.service.product import ProductService
from modules.product.application.dto.product import (
    CreateProductCommand,
    UpdateProductCommand,
    UpdateStockCommand,
    ProductResponse,
    ProductListResponse
)
from shared.interfaces.service_locator import service_locator

product_router = APIRouter()

@product_router.post("", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
@inject
async def create_product(
    command: CreateProductCommand,
    service: ProductService = Depends(Provide[ProductContainer.service]),
    auth_service = Depends(service_locator.get_dependency("auth_service")),
) -> ProductResponse:
    """Crear un nuevo producto."""
    try:
        # Obtener usuario actual
        current_user = await auth_service.get_current_user()
        if not current_user:
            raise HTTPException(401, "Authentication required")
        
        return await service.create_product(command, current_user.id)
    except PermissionError as e:
        raise HTTPException(403, str(e))
    except ValueError as e:
        raise HTTPException(400, str(e))

@product_router.get("", response_model=ProductListResponse)
@inject
async def get_products(
    limit: int = Query(10, ge=1, le=100),
    page: int = Query(0, ge=0),
    service: ProductService = Depends(Provide[ProductContainer.service]),
) -> ProductListResponse:
    """Obtener lista de productos."""
    return await service.get_products(limit, page)

@product_router.get("/{product_id}", response_model=ProductResponse)
@inject
async def get_product(
    product_id: int,
    service: ProductService = Depends(Provide[ProductContainer.service]),
) -> ProductResponse:
    """Obtener un producto por ID."""
    product = await service.get_product_by_id(product_id)
    if not product:
        raise HTTPException(404, "Product not found")
    return product

@product_router.get("/category/{category}", response_model=List[ProductResponse])
@inject
async def get_products_by_category(
    category: str,
    service: ProductService = Depends(Provide[ProductContainer.service]),
) -> List[ProductResponse]:
    """Obtener productos por categoría."""
    return await service.search_products_by_category(category)

@product_router.put("/{product_id}", response_model=ProductResponse)
@inject
async def update_product(
    product_id: int,
    command: UpdateProductCommand,
    service: ProductService = Depends(Provide[ProductContainer.service]),
    auth_service = Depends(service_locator.get_dependency("auth_service")),
) -> ProductResponse:
    """Actualizar un producto."""
    try:
        current_user = await auth_service.get_current_user()
        if not current_user:
            raise HTTPException(401, "Authentication required")
        
        command.id = product_id
        return await service.update_product(command, current_user.id)
    except PermissionError as e:
        raise HTTPException(403, str(e))
    except ValueError as e:
        raise HTTPException(400, str(e))

@product_router.patch("/{product_id}/stock", response_model=ProductResponse)
@inject
async def update_stock(
    product_id: int,
    command: UpdateStockCommand,
    service: ProductService = Depends(Provide[ProductContainer.service]),
) -> ProductResponse:
    """Actualizar stock de un producto."""
    try:
        command.product_id = product_id
        return await service.update_stock(command)
    except ValueError as e:
        raise HTTPException(400, str(e))

@product_router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def delete_product(
    product_id: int,
    service: ProductService = Depends(Provide[ProductContainer.service]),
    auth_service = Depends(service_locator.get_dependency("auth_service")),
):
    """Eliminar un producto."""
    try:
        current_user = await auth_service.get_current_user()
        if not current_user:
            raise HTTPException(401, "Authentication required")
        
        success = await service.delete_product(product_id, current_user.id)
        if not success:
            raise HTTPException(404, "Product not found")
    except PermissionError as e:
        raise HTTPException(403, str(e))
```

## Paso 6: Configuración

### 6.1 Container

```python
# modules/product/container.py
from dependency_injector.providers import Factory, Singleton
from dependency_injector.containers import DeclarativeContainer

from .adapter.output.persistence.repository_adapter import ProductRepositoryAdapter
from .adapter.output.persistence.sqlalchemy.product import ProductSQLAlchemyRepository
from .application.service.product import ProductService
from core.db.session import session

class ProductContainer(DeclarativeContainer):
    """Container de dependencias para el módulo de productos."""
    
    # Repositorio SQLAlchemy
    repository = Singleton(
        ProductSQLAlchemyRepository,
        session=session
    )
    
    # Adaptador del repositorio
    repository_adapter = Factory(
        ProductRepositoryAdapter,
        repository=repository
    )
    
    # Servicio principal
    service = Factory(
        ProductService,
        repository=repository_adapter
    )
```

### 6.2 Definición del Módulo

```python
# modules/product/module.py
from fastapi import APIRouter
from dependency_injector.containers import DeclarativeContainer
from typing import Dict

from shared.interfaces.module_registry import ModuleInterface
from .container import ProductContainer

class ProductModule(ModuleInterface):
    """Módulo de productos."""
    
    def __init__(self):
        self._container = ProductContainer()
        self._routes = self._setup_routes()
    
    @property
    def name(self) -> str:
        return "product"
    
    @property
    def container(self) -> DeclarativeContainer:
        return self._container
    
    @property
    def service(self) -> Dict[str, object]:
        return {
            "product_service": self._container.service,
        }
    
    @property
    def routes(self) -> APIRouter:
        return self._routes
    
    def _setup_routes(self) -> APIRouter:
        """Configurar las rutas del módulo."""
        from .adapter.input.api.v1.product import product_router
        
        router = APIRouter(prefix="/products", tags=["Products"])
        router.include_router(product_router)
        return router
```

## Paso 7: Migración de Base de Datos

```bash
# Crear migración
alembic revision --autogenerate -m "add products table"

# Aplicar migración
alembic upgrade head
```

## Paso 8: Testing

### 8.1 Tests Unitarios

```python
# tests/unit/modules/product/test_product_service.py
import pytest
from unittest.mock import AsyncMock
from decimal import Decimal

from modules.product.application.service.product import ProductService
from modules.product.application.dto.product import CreateProductCommand
from modules.product.domain.entity.product import Product

@pytest.mark.asyncio
async def test_create_product_success():
    # Arrange
    mock_repository = AsyncMock()
    mock_repository.save.return_value = Product(
        id=1,
        name="Test Product",
        price=Decimal('29.99'),
        category="electronics",
        stock=10
    )
    
    service = ProductService(mock_repository)
    command = CreateProductCommand(
        name="Test Product",
        price=Decimal('29.99'),
        category="electronics",
        stock=10
    )
    
    # Mock service_locator
    from shared.interfaces.service_locator import service_locator
    mock_rbac = AsyncMock()
    mock_rbac.get_user_roles.return_value = ["admin"]
    service_locator.register_service("rbac.role_service", mock_rbac)
    
    # Act
    result = await service.create_product(command, "user123")
    
    # Assert
    assert result.name == "Test Product"
    assert result.price == Decimal('29.99')
    mock_repository.save.assert_called_once()

@pytest.mark.asyncio
async def test_create_product_insufficient_permissions():
    # Arrange
    mock_repository = AsyncMock()
    service = ProductService(mock_repository)
    command = CreateProductCommand(
        name="Test Product",
        price=Decimal('29.99'),
        category="electronics",
        stock=10
    )
    
    # Mock RBAC service with insufficient permissions
    mock_rbac = AsyncMock()
    mock_rbac.get_user_roles.return_value = ["user"]  # No admin/manager
    service_locator.register_service("rbac.role_service", mock_rbac)
    
    # Act & Assert
    with pytest.raises(PermissionError):
        await service.create_product(command, "user123")
```

### 8.2 Tests de Integración

```python
# tests/integration/modules/product/test_product_api.py
import pytest
from httpx import AsyncClient
from decimal import Decimal

@pytest.mark.asyncio
async def test_create_product_endpoint(client: AsyncClient, auth_headers):
    response = await client.post(
        "/products",
        json={
            "name": "Integration Test Product",
            "description": "Test description",
            "price": "49.99",
            "category": "test",
            "stock": 5
        },
        headers=auth_headers
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Integration Test Product"
    assert data["price"] == "49.99"
    assert data["stock"] == 5

@pytest.mark.asyncio
async def test_get_products_endpoint(client: AsyncClient):
    response = await client.get("/products")
    
    assert response.status_code == 200
    data = response.json()
    assert "products" in data
    assert "total" in data
    assert isinstance(data["products"], list)
```

## Paso 9: Documentación

### 9.1 README del Módulo

```markdown
# Módulo de Productos

## Descripción
Módulo para la gestión de productos en el sistema.

## Funcionalidades
- ✅ CRUD completo de productos
- ✅ Gestión de stock
- ✅ Búsqueda por categoría
- ✅ Control de permisos basado en roles
- ✅ Validaciones de negocio

## API Endpoints
- `POST /products` - Crear producto
- `GET /products` - Listar productos
- `GET /products/{id}` - Obtener producto
- `PUT /products/{id}` - Actualizar producto
- `PATCH /products/{id}/stock` - Actualizar stock
- `DELETE /products/{id}` - Eliminar producto

## Permisos Requeridos
- **Crear**: admin, manager
- **Leer**: usuario autenticado
- **Actualizar**: creador del producto o admin
- **Eliminar**: admin únicamente
```

## Paso 10: Verificación

### 10.1 Verificar Auto-discovery

```bash
# Iniciar el servidor
python -m hexa api --dev

# Verificar en los logs que aparezca:
# ✅ Found product module
# ˪💼 'product_service' service installed.
```

### 10.2 Probar la API

```bash
# Crear producto
curl -X POST "http://localhost:8000/products" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "name": "Laptop Gaming",
    "description": "High-performance gaming laptop",
    "price": "1299.99",
    "category": "electronics",
    "stock": 5
  }'

# Listar productos
curl "http://localhost:8000/products"

# Buscar por categoría
curl "http://localhost:8000/products/category/electronics"
```

### 10.3 Verificar Documentación

Visita `http://localhost:8000/docs` y verifica que aparezcan los endpoints del módulo de productos.

## Conclusión

¡Felicidades! Has creado un módulo completo siguiendo la arquitectura hexagonal del proyecto. Este módulo incluye:

- ✅ **Arquitectura hexagonal** completa
- ✅ **Dependency injection** configurada
- ✅ **Service locator** para comunicación entre módulos
- ✅ **Validaciones de dominio** y aplicación
- ✅ **Control de permisos** integrado
- ✅ **Tests unitarios** e integración
- ✅ **Documentación** de API automática

## Próximos Pasos

1. **Agregar más funcionalidades**: Categorías, imágenes, reviews
2. **Optimizar performance**: Cache, índices de DB
3. **Agregar eventos**: Notificaciones cuando cambie el stock
4. **Mejorar tests**: Coverage completo, tests de performance
5. **Monitoreo**: Logs estructurados, métricas