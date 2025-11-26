# Guía Rápida: Crear un Nuevo Módulo

Esta guía te ayudará a crear un nuevo módulo en la aplicación usando el enfoque simplificado con variables y funciones.

## 📋 Estructura de un Módulo

Un módulo completo sigue la arquitectura hexagonal y tiene esta estructura:

```
modules/
└── [nombre_modulo]/
    ├── __init__.py
    ├── module.py                    # ⭐ Configuración del módulo (REQUERIDO)
    ├── container.py                 # Dependency Injection Container
    ├── permissions.py               # (Opcional) Definición de permisos
    ├── domain/                      # Capa de Dominio
    │   ├── entity/                  # Entidades del dominio
    │   ├── repository/              # Interfaces de repositorio
    │   └── service/                 # Servicios de dominio (opcional)
    ├── application/                 # Capa de Aplicación
    │   ├── usecase/                 # Casos de uso
    │   └── service/                 # Servicios de aplicación
    └── adapter/                     # Capa de Adaptadores
        ├── input/                   # Adaptadores de entrada
        │   ├── api/v1/              # REST API endpoints
        │   └── tasks/               # Celery tasks (opcional)
        └── output/                  # Adaptadores de salida
            └── persistence/         # Implementaciones de repositorio
                └── sqlalchemy/      # Repositorios SQLAlchemy
```

## 🚀 Paso 1: Crear el archivo `module.py`

Este es el archivo **más importante** y el único **REQUERIDO** para que el módulo sea descubierto.

```python
"""
Módulo de [Nombre del Módulo]
Configuración simplificada usando variables y funciones
"""

from typing import Dict
from fastapi import APIRouter
from modules.[nombre_modulo].container import [Nombre]Container


def setup_routes() -> APIRouter:
    """Configura las rutas del módulo"""
    # Importar routers (lazy import para evitar dependencias circulares)
    from .adapter.input.api.v1.[nombre] import [nombre]_router as [nombre]_v1_router
    
    # Crear router principal
    router = APIRouter(prefix="/[nombre_plural]", tags=["[Nombre Categoría]"])
    
    # Incluir sub-routers
    router.include_router(
        [nombre]_v1_router, 
        prefix="/v1/[nombre_plural]", 
        tags=["[Nombre Categoría]"]
    )
    
    return router


# ========== CONFIGURACIÓN DEL MÓDULO ==========

# Nombre único del módulo (REQUERIDO)
name = "[nombre_modulo]"

# Container de Dependency Injection (RECOMENDADO)
container = [Nombre]Container()

# Servicios expuestos al service_locator (REQUERIDO)
service: Dict[str, object] = {
    "[nombre]_service": container.service,
}

# Rutas del módulo (OPCIONAL - puede ser None si no tiene endpoints HTTP)
routes = setup_routes()
```

### Variables Requeridas

| Variable | Tipo | Requerido | Descripción |
|----------|------|-----------|-------------|
| `name` | `str` | ✅ Sí | Identificador único del módulo |
| `container` | `DeclarativeContainer` | ⚠️ Recomendado | Container de Dependency Injector |
| `service` | `Dict[str, object]` | ✅ Sí | Servicios expuestos (puede ser dict vacío `{}`) |
| `routes` | `APIRouter` \| `None` | ❌ No | Rutas del módulo (usar `None` si no tiene) |

## 🔧 Paso 2: Crear el Container

```python
# modules/[nombre_modulo]/container.py

from dependency_injector.providers import Factory, Singleton
from dependency_injector.containers import DeclarativeContainer, WiringConfiguration

from modules.[nombre_modulo].adapter.output.persistence.repository_adapter import (
    [Nombre]RepositoryAdapter,
)
from modules.[nombre_modulo].adapter.output.persistence.sqlalchemy.[nombre] import (
    [Nombre]SQLAlchemyRepository,
)
from modules.[nombre_modulo].application.service.[nombre] import [Nombre]Service


class [Nombre]Container(DeclarativeContainer):
    """Container de Dependency Injection para el módulo [nombre]"""
    
    wiring_config = WiringConfiguration(packages=["."], auto_wire=True)

    # Repositorio SQLAlchemy (Singleton - una instancia compartida)
    repository = Singleton([Nombre]SQLAlchemyRepository)

    # Adaptador de repositorio (Factory - nueva instancia cada vez)
    repository_adapter = Factory(
        [Nombre]RepositoryAdapter,
        repository=repository,
    )

    # Servicio de aplicación (Factory)
    service = Factory(
        [Nombre]Service,
        repository=repository_adapter,
    )
```

## 📦 Paso 3: Crear la Entidad de Dominio

```python
# modules/[nombre_modulo]/domain/entity/[nombre].py

from sqlmodel import SQLModel, Field
from shared.mixins import AuditMixin, TimestampMixin


class [Nombre](SQLModel, AuditMixin, TimestampMixin, table=True):
    """Entidad de dominio [Nombre]"""
    
    id: int | None = Field(None, primary_key=True)
    name: str = Field(description="Nombre del [nombre]")
    description: str | None = Field(default=None, description="Descripción")
    is_active: bool = Field(default=True, description="Estado activo/inactivo")
    
    # created_at, updated_at, created_by, updated_by se agregan automáticamente
```

## 🔌 Paso 4: Crear el Puerto (Interface) del Repositorio

```python
# modules/[nombre_modulo]/domain/repository/[nombre]_repository.py

from abc import ABC, abstractmethod
from typing import List, Optional
from modules.[nombre_modulo].domain.entity.[nombre] import [Nombre]


class [Nombre]Repository(ABC):
    """Puerto (interface) del repositorio de [Nombre]"""

    @abstractmethod
    async def create(self, [nombre]: [Nombre]) -> [Nombre]:
        """Crea un nuevo [nombre]"""
        pass

    @abstractmethod
    async def get_by_id(self, id: int) -> Optional[[Nombre]]:
        """Obtiene un [nombre] por ID"""
        pass

    @abstractmethod
    async def get_all(self) -> List[[Nombre]]:
        """Obtiene todos los [nombre]s"""
        pass

    @abstractmethod
    async def update(self, [nombre]: [Nombre]) -> [Nombre]:
        """Actualiza un [nombre]"""
        pass

    @abstractmethod
    async def delete(self, id: int) -> bool:
        """Elimina un [nombre]"""
        pass
```

## 🗄️ Paso 5: Implementar el Repositorio SQLAlchemy

```python
# modules/[nombre_modulo]/adapter/output/persistence/sqlalchemy/[nombre].py

from typing import List, Optional
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from core.database.transaction_manager import TransactionManager
from modules.[nombre_modulo].domain.entity.[nombre] import [Nombre]
from modules.[nombre_modulo].domain.repository.[nombre]_repository import [Nombre]Repository


class [Nombre]SQLAlchemyRepository([Nombre]Repository):
    """Implementación SQLAlchemy del repositorio de [Nombre]"""

    def __init__(self):
        self.transaction_manager = TransactionManager()

    async def create(self, [nombre]: [Nombre]) -> [Nombre]:
        async with self.transaction_manager.session() as session:
            session.add([nombre])
            await session.commit()
            await session.refresh([nombre])
            return [nombre]

    async def get_by_id(self, id: int) -> Optional[[Nombre]]:
        async with self.transaction_manager.session() as session:
            statement = select([Nombre]).where([Nombre].id == id)
            result = await session.exec(statement)
            return result.first()

    async def get_all(self) -> List[[Nombre]]:
        async with self.transaction_manager.session() as session:
            statement = select([Nombre])
            result = await session.exec(statement)
            return result.all()

    async def update(self, [nombre]: [Nombre]) -> [Nombre]:
        async with self.transaction_manager.session() as session:
            session.add([nombre])
            await session.commit()
            await session.refresh([nombre])
            return [nombre]

    async def delete(self, id: int) -> bool:
        async with self.transaction_manager.session() as session:
            statement = select([Nombre]).where([Nombre].id == id)
            result = await session.exec(statement)
            [nombre] = result.first()
            if [nombre]:
                await session.delete([nombre])
                await session.commit()
                return True
            return False
```

## 🔄 Paso 6: Crear el Adaptador del Repositorio

```python
# modules/[nombre_modulo]/adapter/output/persistence/repository_adapter.py

from typing import List, Optional
from modules.[nombre_modulo].domain.entity.[nombre] import [Nombre]
from modules.[nombre_modulo].domain.repository.[nombre]_repository import [Nombre]Repository


class [Nombre]RepositoryAdapter:
    """Adaptador del repositorio de [Nombre]"""

    def __init__(self, repository: [Nombre]Repository):
        self._repository = repository

    async def create(self, [nombre]: [Nombre]) -> [Nombre]:
        return await self._repository.create([nombre])

    async def get_by_id(self, id: int) -> Optional[[Nombre]]:
        return await self._repository.get_by_id(id)

    async def get_all(self) -> List[[Nombre]]:
        return await self._repository.get_all()

    async def update(self, [nombre]: [Nombre]) -> [Nombre]:
        return await self._repository.update([nombre])

    async def delete(self, id: int) -> bool:
        return await self._repository.delete(id)
```

## 💼 Paso 7: Crear el Servicio de Aplicación

```python
# modules/[nombre_modulo]/application/service/[nombre].py

from typing import List, Optional
from modules.[nombre_modulo].domain.entity.[nombre] import [Nombre]
from modules.[nombre_modulo].adapter.output.persistence.repository_adapter import (
    [Nombre]RepositoryAdapter,
)


class [Nombre]Service:
    """Servicio de aplicación de [Nombre]"""

    def __init__(self, repository: [Nombre]RepositoryAdapter):
        self._repository = repository

    async def create_[nombre](self, [nombre]: [Nombre]) -> [Nombre]:
        """Crea un nuevo [nombre]"""
        return await self._repository.create([nombre])

    async def get_[nombre]_by_id(self, id: int) -> Optional[[Nombre]]:
        """Obtiene un [nombre] por ID"""
        return await self._repository.get_by_id(id)

    async def get_all_[nombre]s(self) -> List[[Nombre]]:
        """Obtiene todos los [nombre]s"""
        return await self._repository.get_all()

    async def update_[nombre](self, [nombre]: [Nombre]) -> [Nombre]:
        """Actualiza un [nombre]"""
        return await self._repository.update([nombre])

    async def delete_[nombre](self, id: int) -> bool:
        """Elimina un [nombre]"""
        return await self._repository.delete(id)
```

## 🌐 Paso 8: Crear los Endpoints de API

```python
# modules/[nombre_modulo]/adapter/input/api/v1/[nombre].py

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from dependency_injector.wiring import inject, Provide

from modules.[nombre_modulo].application.service.[nombre] import [Nombre]Service
from modules.[nombre_modulo].container import [Nombre]Container
from modules.[nombre_modulo].domain.entity.[nombre] import [Nombre]

[nombre]_router = APIRouter()


@[nombre]_router.post("/", response_model=[Nombre], status_code=status.HTTP_201_CREATED)
@inject
async def create_[nombre](
    [nombre]: [Nombre],
    service: [Nombre]Service = Depends(Provide[[Nombre]Container.service]),
):
    """Crea un nuevo [nombre]"""
    return await service.create_[nombre]([nombre])


@[nombre]_router.get("/{id}", response_model=[Nombre])
@inject
async def get_[nombre](
    id: int,
    service: [Nombre]Service = Depends(Provide[[Nombre]Container.service]),
):
    """Obtiene un [nombre] por ID"""
    [nombre] = await service.get_[nombre]_by_id(id)
    if not [nombre]:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="[Nombre] not found"
        )
    return [nombre]


@[nombre]_router.get("/", response_model=List[[Nombre]])
@inject
async def get_all_[nombre]s(
    service: [Nombre]Service = Depends(Provide[[Nombre]Container.service]),
):
    """Obtiene todos los [nombre]s"""
    return await service.get_all_[nombre]s()


@[nombre]_router.put("/{id}", response_model=[Nombre])
@inject
async def update_[nombre](
    id: int,
    [nombre]: [Nombre],
    service: [Nombre]Service = Depends(Provide[[Nombre]Container.service]),
):
    """Actualiza un [nombre]"""
    [nombre].id = id
    return await service.update_[nombre]([nombre])


@[nombre]_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def delete_[nombre](
    id: int,
    service: [Nombre]Service = Depends(Provide[[Nombre]Container.service]),
):
    """Elimina un [nombre]"""
    deleted = await service.delete_[nombre](id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="[Nombre] not found"
        )
```

## 🔐 Paso 9: (Opcional) Definir Permisos

```python
# modules/[nombre_modulo]/permissions.py

from core.rbac.permissions import PermissionGroup


class [Nombre]Permissions(PermissionGroup):
    """Permisos del módulo [nombre_modulo]"""
    
    module_name = "[nombre_modulo]"
    
    # Definir permisos
    CREATE = "create_[nombre]"
    READ = "read_[nombre]"
    UPDATE = "update_[nombre]"
    DELETE = "delete_[nombre]"
    LIST = "list_[nombre]s"
```

## ✅ Verificación

Después de crear todos los archivos, verifica que el módulo se registre correctamente:

```bash
cd backend
python -c "
from shared.interfaces.module_discovery import discover_modules
from shared.interfaces.module_registry import ModuleRegistry
from shared.interfaces.service_locator import service_locator

ModuleRegistry().clear()
service_locator.clear()

discover_modules('modules', 'module.py')
"
```

Deberías ver algo como:

```
✅ Found '[nombre_modulo]' module
 ˪💼 '[nombre]_service' service installed.

======================================================================
📦 RESUMEN DE MÓDULOS REGISTRADOS
======================================================================
...
   • [nombre_modulo]           [Type: SimpleModule   ] Routes: ✓  Container: ✓
...
```

## 🎯 Casos Especiales

### Módulo sin Rutas HTTP

Si tu módulo no expone endpoints HTTP (ej: solo servicios internos):

```python
# module.py
name = "background_jobs"
container = BackgroundJobsContainer()
service: Dict[str, object] = {
    "job_service": container.job_service,
}
routes = None  # Sin rutas HTTP
```

### Módulo con Celery Tasks

```python
# module.py
from modules.[nombre].adapter.input.tasks.[nombre] import process_[nombre]_task

name = "[nombre]"
container = [Nombre]Container()
service: Dict[str, object] = {
    "[nombre]_service": container.service,
    "[nombre]_tasks": {
        "process_[nombre]_task": {
            "task": process_[nombre]_task,
            "config": {
                "autoretry_for": (Exception,),
                "retry_kwargs": {"max_retries": 5},
                "retry_backoff": True,
                "retry_backoff_max": 600,
                "retry_jitter": True,
            },
        }
    },
}
routes = setup_routes()
```

### Módulo con Múltiples Servicios

```python
# module.py
service: Dict[str, object] = {
    "[nombre]_service": container.service,
    "[nombre].specialized_service": container.specialized_service,
    "[nombre].helper_service": container.helper_service,
}
```

### Módulo con Múltiples Routers

```python
def setup_routes() -> APIRouter:
    """Configura las rutas del módulo"""
    from .adapter.input.api.v1.main import main_router
    from .adapter.input.api.v1.secondary import secondary_router
    from .adapter.input.api.v1.admin import admin_router
    
    router = APIRouter(prefix="/[nombre]", tags=["[Nombre]"])
    router.include_router(main_router, prefix="/v1/main")
    router.include_router(secondary_router, prefix="/v1/secondary")
    router.include_router(admin_router, prefix="/v1/admin")
    
    return router
```

## 📚 Recursos Adicionales

- [Arquitectura de Módulos](../architecture/02-project-structure.md)
- [Simplificación del Sistema de Módulos](../architecture/05-module-simplification.md)
- [Service Locator Pattern](../architecture/04-service-locator.md)
- [Testing de Repositorios](../TESTING_REPOSITORY_FIX.md)

## 🐛 Troubleshooting

### El módulo no se descubre

- Verifica que el archivo se llame exactamente `module.py`
- Verifica que la variable `name` esté definida
- Verifica que no haya errores de sintaxis o importación

### Error "Module already registered"

- El nombre del módulo debe ser único
- Usa `ModuleRegistry().clear()` antes de `discover_modules()` en tests

### Servicios no disponibles en service_locator

- Verifica que los servicios estén en el diccionario `service`
- Verifica que el container esté correctamente configurado
- Revisa que no haya dependencias circulares

## ✨ Tips

1. **Lazy Imports**: Importa routers dentro de `setup_routes()` para evitar dependencias circulares
2. **Naming Convention**: Usa nombres consistentes en todo el módulo
3. **Type Hints**: Siempre usa type hints para mejor autocompletado y detección de errores
4. **Docstrings**: Documenta todas las funciones y clases públicas
5. **Tests**: Crea tests para cada componente del módulo