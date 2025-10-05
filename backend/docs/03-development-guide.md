# Guía de Desarrollo

## Procedimiento para Nuevo Desarrollo

### 1. Análisis y Planificación

Antes de comenzar, define:
- **Dominio**: ¿Qué entidad o concepto de negocio vas a modelar?
- **Casos de uso**: ¿Qué operaciones necesitas?
- **Dependencias**: ¿Qué otros módulos necesitas?
- **Persistencia**: ¿Qué datos necesitas almacenar?

### 2. Crear la Estructura del Módulo

```bash
# Crear estructura básica
mkdir -p modules/[module_name]/{adapter/{input/api/v1,output/persistence},application/{service,dto},domain/{entity,repository,usecase}}

# Archivos principales
touch modules/[module_name]/{__init__.py,container.py,module.py}
```

### 3. Definir el Dominio

#### 3.1 Entidades
```python
# modules/[module_name]/domain/entity/[entity].py
from dataclasses import dataclass
from typing import Optional

@dataclass
class Product:
    id: Optional[int] = None
    name: str = ""
    price: float = 0.0
    active: bool = True
```

#### 3.2 Interfaces de Repositorio
```python
# modules/[module_name]/domain/repository/[entity].py
from abc import ABC, abstractmethod
from typing import List, Optional
from ..entity.product import Product

class ProductRepositoryInterface(ABC):
    @abstractmethod
    async def save(self, product: Product) -> Product:
        pass
    
    @abstractmethod
    async def find_by_id(self, id: int) -> Optional[Product]:
        pass
    
    @abstractmethod
    async def find_all(self) -> List[Product]:
        pass
```

### 4. Implementar la Capa de Aplicación

#### 4.1 DTOs y Comandos
```python
# modules/[module_name]/application/dto/product.py
from pydantic import BaseModel

class CreateProductCommand(BaseModel):
    name: str
    price: float

class ProductResponse(BaseModel):
    id: int
    name: str
    price: float
    active: bool
```

#### 4.2 Servicios
```python
# modules/[module_name]/application/service/product.py
from typing import List
from ..dto.product import CreateProductCommand, ProductResponse
from ...domain.repository.product import ProductRepositoryInterface
from ...domain.entity.product import Product

class ProductService:
    def __init__(self, repository: ProductRepositoryInterface):
        self.repository = repository
    
    async def create_product(self, command: CreateProductCommand) -> ProductResponse:
        product = Product(
            name=command.name,
            price=command.price
        )
        saved_product = await self.repository.save(product)
        return ProductResponse(**saved_product.__dict__)
    
    async def get_all_products(self) -> List[ProductResponse]:
        products = await self.repository.find_all()
        return [ProductResponse(**p.__dict__) for p in products]
```

### 5. Implementar Adaptadores

#### 5.1 Repositorio (Output Adapter)
```python
# modules/[module_name]/adapter/output/persistence/repository_adapter.py
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from ....domain.repository.product import ProductRepositoryInterface
from ....domain.entity.product import Product
from .sqlalchemy.product import ProductSQLAlchemyRepository

class ProductRepositoryAdapter(ProductRepositoryInterface):
    def __init__(self, repository: ProductSQLAlchemyRepository):
        self.repository = repository
    
    async def save(self, product: Product) -> Product:
        return await self.repository.save(product)
    
    async def find_by_id(self, id: int) -> Optional[Product]:
        return await self.repository.find_by_id(id)
    
    async def find_all(self) -> List[Product]:
        return await self.repository.find_all()
```

#### 5.2 API (Input Adapter)
```python
# modules/[module_name]/adapter/input/api/v1/product.py
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from typing import List

from ...container import ProductContainer
from ....application.service.product import ProductService
from ....application.dto.product import CreateProductCommand, ProductResponse

product_router = APIRouter()

@product_router.post("", response_model=ProductResponse)
@inject
async def create_product(
    command: CreateProductCommand,
    service: ProductService = Depends(Provide[ProductContainer.service])
) -> ProductResponse:
    return await service.create_product(command)

@product_router.get("", response_model=List[ProductResponse])
@inject
async def get_products(
    service: ProductService = Depends(Provide[ProductContainer.service])
) -> List[ProductResponse]:
    return await service.get_all_products()
```

### 6. Configurar Dependency Injection

```python
# modules/[module_name]/container.py
from dependency_injector.providers import Factory, Singleton
from dependency_injector.containers import DeclarativeContainer

from .adapter.output.persistence.repository_adapter import ProductRepositoryAdapter
from .adapter.output.persistence.sqlalchemy.product import ProductSQLAlchemyRepository
from .application.service.product import ProductService

class ProductContainer(DeclarativeContainer):
    repository = Singleton(ProductSQLAlchemyRepository)
    repository_adapter = Factory(ProductRepositoryAdapter, repository=repository)
    service = Factory(ProductService, repository=repository_adapter)
```

### 7. Definir el Módulo

```python
# modules/[module_name]/module.py
from fastapi import APIRouter
from dependency_injector.containers import DeclarativeContainer
from typing import Dict

from shared.interfaces.module_registry import ModuleInterface
from .container import ProductContainer

class ProductModule(ModuleInterface):
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
        return {"product_service": self._container.service}
    
    @property
    def routes(self) -> APIRouter:
        return self._routes
    
    def _setup_routes(self) -> APIRouter:
        from .adapter.input.api.v1.product import product_router
        
        router = APIRouter(prefix="/products", tags=["Products"])
        router.include_router(product_router)
        return router
```

### 8. Testing

#### 8.1 Test de Unidad
```python
# tests/modules/[module_name]/test_product_service.py
import pytest
from unittest.mock import AsyncMock

from modules.product.application.service.product import ProductService
from modules.product.application.dto.product import CreateProductCommand
from modules.product.domain.entity.product import Product

@pytest.mark.asyncio
async def test_create_product():
    # Arrange
    mock_repository = AsyncMock()
    mock_repository.save.return_value = Product(id=1, name="Test", price=10.0)
    
    service = ProductService(mock_repository)
    command = CreateProductCommand(name="Test", price=10.0)
    
    # Act
    result = await service.create_product(command)
    
    # Assert
    assert result.name == "Test"
    assert result.price == 10.0
    mock_repository.save.assert_called_once()
```

#### 8.2 Test de Integración
```python
# tests/modules/[module_name]/test_product_api.py
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_create_product_endpoint(client: AsyncClient):
    response = await client.post(
        "/products",
        json={"name": "Test Product", "price": 29.99}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Product"
    assert data["price"] == 29.99
```

## Flujo de Desarrollo Recomendado

1. **Domain First**: Empieza por las entidades y reglas de negocio
2. **Test Driven**: Escribe tests antes de la implementación
3. **Outside-In**: Desde la API hacia el dominio
4. **Iterativo**: Implementa funcionalidad básica primero
5. **Refactoring**: Mejora continuamente el diseño

## Herramientas de Desarrollo

```bash
# Linting y formateo
ruff check .
ruff format .

# Tests
pytest

# Coverage
pytest --cov=modules

# Migraciones
alembic revision --autogenerate -m "add product table"
alembic upgrade head
```