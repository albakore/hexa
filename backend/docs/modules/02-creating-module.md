# Crear un Nuevo Módulo - Guía Completa

Esta guía te llevará paso a paso para crear un módulo completamente funcional, basándose en la estructura real del proyecto.

## Pre-requisitos

- Entender [Arquitectura Hexagonal](../architecture/01-overview.md)
- Conocer [Estructura del Proyecto](../architecture/02-project-structure.md)
- Tener el proyecto corriendo localmente

## Ejemplo: Módulo de Productos

Vamos a crear un módulo completo de "Productos" desde cero.

## Paso 1: Crear Estructura de Carpetas

```bash
cd modules/

# Crear estructura completa
mkdir -p product/{domain/{entity,repository,usecase},application/service,adapter/{input/{api/v1,tasks},output/persistence/sqlalchemy},test}

# Crear archivos __init__.py
touch product/__init__.py
touch product/domain/__init__.py
touch product/domain/entity/__init__.py
touch product/domain/repository/__init__.py
touch product/domain/usecase/__init__.py
touch product/application/__init__.py
touch product/application/service/__init__.py
touch product/adapter/__init__.py
touch product/adapter/input/__init__.py
touch product/adapter/input/api/__init__.py
touch product/adapter/input/api/v1/__init__.py
touch product/adapter/input/tasks/__init__.py
touch product/adapter/output/__init__.py
touch product/adapter/output/persistence/__init__.py
touch product/test/__init__.py
```

**Resultado**:
```
modules/product/
├── __init__.py
├── domain/
│   ├── __init__.py
│   ├── entity/
│   │   └── __init__.py
│   ├── repository/
│   │   └── __init__.py
│   └── usecase/
│       └── __init__.py
├── application/
│   ├── __init__.py
│   └── service/
│       └── __init__.py
├── adapter/
│   ├── __init__.py
│   ├── input/
│   │   ├── __init__.py
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   └── v1/
│   │   │       └── __init__.py
│   │   └── tasks/
│   │       └── __init__.py
│   └── output/
│       ├── __init__.py
│       └── persistence/
│           ├── __init__.py
│           └── sqlalchemy/
└── test/
    └── __init__.py
```

## Paso 2: Definir Entidad de Dominio

```python
# modules/product/domain/entity/product.py
from sqlmodel import SQLModel, Field
from datetime import datetime

class Product(SQLModel, table=True):
    """Entidad de dominio - Producto"""
    __tablename__ = "product"
    
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(min_length=1, max_length=200)
    description: str | None = None
    price: float = Field(gt=0)
    stock: int = Field(default=0, ge=0)
    active: bool = Field(default=True)
    created_at: datetime | None = Field(default_factory=datetime.now)
    updated_at: datetime | None = None
    
    def deactivate(self):
        """Regla de negocio: desactivar producto"""
        self.active = False
    
    def update_stock(self, quantity: int):
        """Regla de negocio: actualizar stock"""
        if self.stock + quantity < 0:
            raise ValueError("Stock cannot be negative")
        self.stock += quantity
```

**Agregar al __init__.py**:
```python
# modules/product/domain/entity/__init__.py
from .product import Product

__all__ = ["Product"]
```

## Paso 3: Definir Repository (Port/Interface)

```python
# modules/product/domain/repository/product.py
from abc import ABC, abstractmethod
from modules.product.domain.entity import Product

class ProductRepository(ABC):
    """Port - Interface del repositorio de productos"""
    
    @abstractmethod
    async def get_product_by_id(self, id: int) -> Product | None:
        """Obtiene un producto por ID"""
        pass
    
    @abstractmethod
    async def get_product_list(self, limit: int, page: int) -> list[Product]:
        """Lista productos paginados"""
        pass
    
    @abstractmethod
    async def get_active_products(self) -> list[Product]:
        """Obtiene productos activos"""
        pass
    
    @abstractmethod
    async def save_product(self, product: Product) -> Product:
        """Guarda o actualiza un producto"""
        pass
    
    @abstractmethod
    async def delete_product(self, id: int) -> bool:
        """Elimina un producto"""
        pass
```

## Paso 4: Implementar Repository con SQLAlchemy

```python
# modules/product/adapter/output/persistence/sqlalchemy/product.py
from sqlmodel import select
from core.db import session as global_session
from modules.product.domain.entity import Product
from modules.product.domain.repository.product import ProductRepository

class ProductSQLAlchemyRepository(ProductRepository):
    """Implementación SQLAlchemy del repositorio"""
    
    async def get_product_by_id(self, id: int) -> Product | None:
        query = select(Product).where(Product.id == id)
        result = await global_session.execute(query)
        return result.scalars().first()
    
    async def get_product_list(self, limit: int, page: int) -> list[Product]:
        offset = page * limit
        query = select(Product).offset(offset).limit(limit)
        result = await global_session.execute(query)
        return list(result.scalars().all())
    
    async def get_active_products(self) -> list[Product]:
        query = select(Product).where(Product.active == True)
        result = await global_session.execute(query)
        return list(result.scalars().all())
    
    async def save_product(self, product: Product) -> Product:
        global_session.add(product)
        await global_session.flush()
        await global_session.refresh(product)
        return product
    
    async def delete_product(self, id: int) -> bool:
        product = await self.get_product_by_id(id)
        if product:
            await global_session.delete(product)
            await global_session.flush()
            return True
        return False
```

## Paso 5: Crear Adapter Wrapper

```python
# modules/product/adapter/output/persistence/product_adapter.py
from dataclasses import dataclass
from modules.product.domain.entity import Product
from modules.product.domain.repository.product import ProductRepository

@dataclass
class ProductRepositoryAdapter(ProductRepository):
    """Adapter que wrappea el repository SQLAlchemy"""
    repository: ProductRepository
    
    async def get_product_by_id(self, id: int) -> Product | None:
        return await self.repository.get_product_by_id(id)
    
    async def get_product_list(self, limit: int, page: int) -> list[Product]:
        return await self.repository.get_product_list(limit, page)
    
    async def get_active_products(self) -> list[Product]:
        return await self.repository.get_active_products()
    
    async def save_product(self, product: Product) -> Product:
        return await self.repository.save_product(product)
    
    async def delete_product(self, id: int) -> bool:
        return await self.repository.delete_product(id)
```

## Paso 6: Crear Use Cases

```python
# modules/product/domain/usecase/product.py
from modules.product.domain.entity import Product
from modules.product.domain.repository.product import ProductRepository

class ProductNotFoundError(Exception):
    pass

class GetProductById:
    """Use Case: Obtener producto por ID"""
    def __init__(self, repository: ProductRepository):
        self.repository = repository
    
    async def execute(self, id: int) -> Product:
        product = await self.repository.get_product_by_id(id)
        if not product:
            raise ProductNotFoundError(f"Product {id} not found")
        return product

class CreateProduct:
    """Use Case: Crear nuevo producto"""
    def __init__(self, repository: ProductRepository):
        self.repository = repository
    
    async def execute(self, data: dict) -> Product:
        product = Product(**data)
        return await self.repository.save_product(product)

class UpdateProductStock:
    """Use Case: Actualizar stock de producto"""
    def __init__(self, repository: ProductRepository):
        self.repository = repository
    
    async def execute(self, id: int, quantity: int) -> Product:
        product = await self.repository.get_product_by_id(id)
        if not product:
            raise ProductNotFoundError(f"Product {id} not found")
        
        product.update_stock(quantity)  # Regla de negocio
        return await self.repository.save_product(product)

class ProductUseCaseFactory:
    """Factory para crear use cases"""
    def __init__(self, repository: ProductRepository):
        self.repository = repository
    
    def get_product_by_id(self) -> GetProductById:
        return GetProductById(self.repository)
    
    def create_product(self) -> CreateProduct:
        return CreateProduct(self.repository)
    
    def update_product_stock(self) -> UpdateProductStock:
        return UpdateProductStock(self.repository)
```

## Paso 7: Crear Service

```python
# modules/product/application/service/product.py
from modules.product.domain.entity import Product
from modules.product.domain.repository.product import ProductRepository
from modules.product.domain.usecase.product import ProductUseCaseFactory

class ProductService:
    """Servicio de aplicación para productos"""
    def __init__(self, product_repository: ProductRepository):
        self.repository = product_repository
        self.usecase_factory = ProductUseCaseFactory(product_repository)
    
    async def get_product_by_id(self, id: int) -> Product:
        """Obtiene producto por ID"""
        usecase = self.usecase_factory.get_product_by_id()
        return await usecase.execute(id)
    
    async def get_product_list(self, limit: int = 10, page: int = 0) -> list[Product]:
        """Lista productos paginados"""
        return await self.repository.get_product_list(limit, page)
    
    async def create_product(self, data: dict) -> Product:
        """Crea un nuevo producto"""
        usecase = self.usecase_factory.create_product()
        return await usecase.execute(data)
    
    async def update_product_stock(self, id: int, quantity: int) -> Product:
        """Actualiza stock de un producto"""
        usecase = self.usecase_factory.update_product_stock()
        return await usecase.execute(id, quantity)
```

## Paso 8: Crear Container de DI

```python
# modules/product/container.py
from dependency_injector.containers import DeclarativeContainer, WiringConfiguration
from dependency_injector.providers import Factory, Singleton

from modules.product.adapter.output.persistence.product_adapter import (
    ProductRepositoryAdapter,
)
from modules.product.adapter.output.persistence.sqlalchemy.product import (
    ProductSQLAlchemyRepository,
)
from modules.product.application.service.product import ProductService

class ProductContainer(DeclarativeContainer):
    wiring_config = WiringConfiguration(packages=["."], auto_wire=True)
    
    # Repository SQLAlchemy
    product_sqlalchemy_repo = Singleton(ProductSQLAlchemyRepository)
    
    # Repository Adapter
    product_repo_adapter = Factory(
        ProductRepositoryAdapter,
        repository=product_sqlalchemy_repo
    )
    
    # Application Service
    product_service = Factory(
        ProductService,
        product_repository=product_repo_adapter
    )
```

## Paso 9: Crear API Endpoints

```python
# modules/product/adapter/input/api/v1/product.py
from fastapi import APIRouter, HTTPException, Depends
from dependency_injector.wiring import inject, Provide

from modules.product.application.service.product import ProductService
from modules.product.domain.usecase.product import ProductNotFoundError

router = APIRouter()

@router.get("/{product_id}")
@inject
async def get_product(
    product_id: int,
    service: ProductService = Depends(Provide["product_container.product_service"])
):
    """Obtiene un producto por ID"""
    try:
        product = await service.get_product_by_id(product_id)
        return product
    except ProductNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/")
@inject
async def list_products(
    limit: int = 10,
    page: int = 0,
    service: ProductService = Depends(Provide["product_container.product_service"])
):
    """Lista productos paginados"""
    products = await service.get_product_list(limit, page)
    return products

@router.post("/")
@inject
async def create_product(
    data: dict,
    service: ProductService = Depends(Provide["product_container.product_service"])
):
    """Crea un nuevo producto"""
    product = await service.create_product(data)
    return product

@router.patch("/{product_id}/stock")
@inject
async def update_stock(
    product_id: int,
    quantity: int,
    service: ProductService = Depends(Provide["product_container.product_service"])
):
    """Actualiza el stock de un producto"""
    try:
        product = await service.update_product_stock(product_id, quantity)
        return product
    except ProductNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
```

## Paso 10: Crear Module.py (Registro)

```python
# modules/product/module.py
from fastapi import APIRouter
from dependency_injector.containers import DeclarativeContainer
from shared.interfaces.module_registry import ModuleInterface
from modules.product.container import ProductContainer
from typing import Dict

class ProductModule(ModuleInterface):
    """Módulo de Productos"""
    
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
            "product_service": self._container.product_service,
        }
    
    @property
    def routes(self) -> APIRouter:
        return self._routes
    
    def _setup_routes(self) -> APIRouter:
        """Configura las rutas del módulo"""
        from .adapter.input.api.v1.product import router as product_v1_router
        
        router = APIRouter(prefix="/product", tags=["Product"])
        router.include_router(product_v1_router, prefix="/v1")
        
        return router
```

## Paso 11: Crear Migración de Base de Datos

```bash
# Crear migración automática
docker compose -f compose.dev.yaml exec backend alembic revision --autogenerate -m "add product table"

# Aplicar migración
docker compose -f compose.dev.yaml exec backend alembic upgrade head
```

## Paso 12: Verificar que Funciona

### 12.1 Reiniciar Backend

```bash
docker compose -f compose.dev.yaml restart backend

# Ver logs
docker compose -f compose.dev.yaml logs backend | grep "product"

# Deberías ver:
# ✅ Found product module
#  ˪💼 'product_service' service installed.
```

### 12.2 Verificar en /docs

- Abrir: http://localhost:8000/api/docs
- Buscar tag "Product"
- Deberías ver todos tus endpoints

### 12.3 Probar Endpoints

```bash
# Crear producto
curl -X POST "http://localhost:8000/api/product/v1/" \
  -H "Content-Type: application/json" \
  -d '{"name": "Test Product", "price": 99.99, "stock": 10}'

# Listar productos
curl "http://localhost:8000/api/product/v1/?limit=10&page=0"

# Obtener por ID
curl "http://localhost:8000/api/product/v1/1"

# Actualizar stock
curl -X PATCH "http://localhost:8000/api/product/v1/1/stock?quantity=5"
```

## (Opcional) Paso 13: Agregar Tasks de Celery

```python
# modules/product/adapter/input/tasks/product.py
def sync_product_inventory():
    """Task para sincronizar inventario"""
    print("Syncing product inventory...")
    return "Inventory synced"

def notify_low_stock(product_id: int):
    """Task para notificar stock bajo"""
    print(f"Notifying low stock for product {product_id}")
    return "Notification sent"
```

**Registrar en module.py**:
```python
@property
def service(self) -> Dict[str, object]:
    from .adapter.input.tasks import product
    
    return {
        "product_service": self._container.product_service,
        "product_tasks": {
            "sync_product_inventory": product.sync_product_inventory,
            "notify_low_stock": product.notify_low_stock,
        },
    }
```

**Reiniciar Celery**:
```bash
docker compose -f compose.dev.yaml restart celery_worker

# Verificar
docker compose -f compose.dev.yaml logs celery_worker | grep "product"

# Deberías ver:
# ✓ Registered: product.sync_product_inventory
# ✓ Registered: product.notify_low_stock
```

## (Opcional) Paso 14: Agregar Tests

```python
# modules/product/test/conftest.py
import pytest

@pytest.fixture
def real_product_repository(db_session):
    """Repositorio real para tests de integración"""
    from modules.product.adapter.output.persistence.sqlalchemy.product import (
        ProductSQLAlchemyRepository,
    )
    from modules.product.adapter.output.persistence.product_adapter import (
        ProductRepositoryAdapter,
    )
    
    sqlalchemy_repo = ProductSQLAlchemyRepository()
    return ProductRepositoryAdapter(repository=sqlalchemy_repo)

@pytest.fixture
def sample_product_data(fake):
    """Datos de ejemplo para un producto"""
    return {
        "name": fake.word(),
        "description": fake.sentence(),
        "price": float(fake.random_int(min=10, max=1000)),
        "stock": fake.random_int(min=0, max=100),
    }
```

```python
# modules/product/test/test_product_repository.py
import pytest
from modules.product.domain.entity import Product

@pytest.mark.integration
@pytest.mark.asyncio
class TestProductRepository:
    async def test_save_product(
        self,
        db_session,
        real_product_repository,
        sample_product_data,
    ):
        """Test: Guardar un producto"""
        product = Product(**sample_product_data)
        
        saved = await real_product_repository.save_product(product)
        
        assert saved.id is not None
        assert saved.name == product.name
```

**Ejecutar tests**:
```bash
docker compose -f compose.dev.yaml exec backend pytest modules/product/test/ -v
```

## Checklist Final

- [ ] Estructura de carpetas creada
- [ ] Entidad definida
- [ ] Repository interface creada
- [ ] Repository SQLAlchemy implementado
- [ ] Adapter creado
- [ ] Use cases implementados
- [ ] Service creado
- [ ] Container configurado
- [ ] Endpoints API creados
- [ ] Module.py implementado
- [ ] Migración creada y aplicada
- [ ] Módulo aparece en logs al iniciar
- [ ] Endpoints aparecen en /docs
- [ ] Endpoints funcionan correctamente
- [ ] (Opcional) Tasks de Celery
- [ ] (Opcional) Tests implementados

## Troubleshooting

### Módulo no aparece en logs

1. Verificar que `module.py` existe y tiene la clase correcta
2. Verificar que implementa `ModuleInterface`
3. Reiniciar backend: `docker compose restart backend`

### Endpoints no aparecen en /docs

1. Verificar que `_setup_routes()` retorna un `APIRouter`
2. Verificar que el router tiene prefix y tags
3. Verificar imports en `module.py`

### Error "Service not found"

1. Verificar que el servicio está en el `@property service`
2. Verificar nombre del servicio
3. Reiniciar backend

### Tests fallan

1. Verificar fixture `real_product_repository`
2. Verificar que `db_session` está disponible
3. Ver [Testing Repository Fix](../../TESTING_REPOSITORY_FIX.md)

## Próximos Pasos

- [Auto-registro de Módulos](./03-module-registry.md)
- [Service Locator](../architecture/04-service-locator.md)
- [Testing](../testing/01-strategy.md)
- [Buenas Prácticas](../best-practices/BEST_PRACTICES.md)
