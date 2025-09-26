# Creación de Nuevos Módulos

## Guía Paso a Paso

Esta guía te llevará a través del proceso completo de creación de un nuevo módulo siguiendo la arquitectura hexagonal desacoplada.

## Paso 1: Estructura Base del Módulo

### Crear Directorio del Módulo
```bash
# Crear estructura básica
mkdir -p modules/mi_modulo/{domain,application,adapter}
mkdir -p modules/mi_modulo/domain/{entity,repository,usecase,vo,exception}
mkdir -p modules/mi_modulo/application/{service,dto,exception}
mkdir -p modules/mi_modulo/adapter/{input,output}
mkdir -p modules/mi_modulo/adapter/input/api/v1/{request,response}
mkdir -p modules/mi_modulo/adapter/output/persistence/{sqlalchemy}

# Crear archivos __init__.py
find modules/mi_modulo -type d -exec touch {}/__init__.py \;
```

### Estructura Final
```
modules/mi_modulo/
├── domain/
│   ├── entity/
│   │   ├── __init__.py
│   │   └── mi_entidad.py
│   ├── repository/
│   │   ├── __init__.py
│   │   └── mi_repository.py
│   ├── usecase/
│   │   ├── __init__.py
│   │   └── mi_usecase.py
│   ├── vo/
│   │   └── __init__.py
│   └── exception/
│       ├── __init__.py
│       └── mi_exceptions.py
├── application/
│   ├── service/
│   │   ├── __init__.py
│   │   └── mi_service.py
│   ├── dto/
│   │   ├── __init__.py
│   │   └── mi_dto.py
│   └── exception/
│       ├── __init__.py
│       └── mi_app_exceptions.py
├── adapter/
│   ├── input/
│   │   └── api/
│   │       └── v1/
│   │           ├── request/
│   │           │   ├── __init__.py
│   │           │   └── mi_request.py
│   │           ├── response/
│   │           │   ├── __init__.py
│   │           │   └── mi_response.py
│   │           ├── __init__.py
│   │           └── mi_controller.py
│   └── output/
│       └── persistence/
│           ├── sqlalchemy/
│           │   ├── __init__.py
│           │   └── mi_repository.py
│           ├── __init__.py
│           └── repository_adapter.py
├── container.py
└── module.py
```

## Paso 2: Implementar el Dominio

### Entidad de Dominio
```python
# modules/mi_modulo/domain/entity/mi_entidad.py
from datetime import datetime
from typing import Optional

class MiEntidad:
    """Entidad de dominio para Mi Módulo"""
    
    def __init__(self, nombre: str, descripcion: str):
        self.id: Optional[int] = None
        self.nombre = self._validate_nombre(nombre)
        self.descripcion = descripcion
        self.activo = True
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
    
    def _validate_nombre(self, nombre: str) -> str:
        """Validar nombre de la entidad"""
        if not nombre or len(nombre.strip()) == 0:
            raise ValueError("El nombre no puede estar vacío")
        
        if len(nombre) > 100:
            raise ValueError("El nombre no puede exceder 100 caracteres")
        
        return nombre.strip()
    
    def actualizar_descripcion(self, nueva_descripcion: str) -> None:
        """Actualizar descripción de la entidad"""
        self.descripcion = nueva_descripcion
        self.updated_at = datetime.now()
    
    def desactivar(self) -> None:
        """Desactivar la entidad"""
        self.activo = False
        self.updated_at = datetime.now()
    
    def activar(self) -> None:
        """Activar la entidad"""
        self.activo = True
        self.updated_at = datetime.now()
    
    def __str__(self) -> str:
        return f"MiEntidad(id={self.id}, nombre='{self.nombre}')"
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, MiEntidad):
            return False
        return self.id == other.id if self.id else False
```

### Value Objects
```python
# modules/mi_modulo/domain/vo/mi_value_object.py
from dataclasses import dataclass
from typing import Union

@dataclass(frozen=True)
class MiValueObject:
    """Value Object para Mi Módulo"""
    valor: str
    tipo: str
    
    def __post_init__(self):
        if not self.valor:
            raise ValueError("El valor no puede estar vacío")
        
        if self.tipo not in ["tipo1", "tipo2", "tipo3"]:
            raise ValueError("Tipo no válido")
    
    def es_tipo(self, tipo: str) -> bool:
        """Verificar si es de un tipo específico"""
        return self.tipo == tipo
    
    def __str__(self) -> str:
        return f"{self.tipo}:{self.valor}"
```

### Repository Interface
```python
# modules/mi_modulo/domain/repository/mi_repository.py
from abc import ABC, abstractmethod
from typing import List, Optional
from modules.mi_modulo.domain.entity.mi_entidad import MiEntidad

class MiRepository(ABC):
    """Interface del repositorio para Mi Entidad"""
    
    @abstractmethod
    def save(self, entidad: MiEntidad) -> MiEntidad:
        """Guardar entidad"""
        pass
    
    @abstractmethod
    def find_by_id(self, entidad_id: int) -> Optional[MiEntidad]:
        """Buscar entidad por ID"""
        pass
    
    @abstractmethod
    def find_by_nombre(self, nombre: str) -> Optional[MiEntidad]:
        """Buscar entidad por nombre"""
        pass
    
    @abstractmethod
    def find_all_active(self) -> List[MiEntidad]:
        """Obtener todas las entidades activas"""
        pass
    
    @abstractmethod
    def delete(self, entidad_id: int) -> bool:
        """Eliminar entidad"""
        pass
    
    @abstractmethod
    def exists_by_nombre(self, nombre: str) -> bool:
        """Verificar si existe una entidad con el nombre dado"""
        pass
```

### Casos de Uso
```python
# modules/mi_modulo/domain/usecase/mi_usecase.py
from modules.mi_modulo.domain.entity.mi_entidad import MiEntidad
from modules.mi_modulo.domain.repository.mi_repository import MiRepository
from modules.mi_modulo.domain.exception.mi_exceptions import (
    MiEntidadAlreadyExistsError, MiEntidadNotFoundError
)

class CrearMiEntidadUseCase:
    """Caso de uso para crear Mi Entidad"""
    
    def __init__(self, repository: MiRepository):
        self.repository = repository
    
    def execute(self, nombre: str, descripcion: str) -> MiEntidad:
        """Ejecutar caso de uso"""
        # Verificar que no existe
        if self.repository.exists_by_nombre(nombre):
            raise MiEntidadAlreadyExistsError(f"Ya existe una entidad con nombre '{nombre}'")
        
        # Crear entidad
        entidad = MiEntidad(nombre, descripcion)
        
        # Guardar
        return self.repository.save(entidad)

class ActualizarMiEntidadUseCase:
    """Caso de uso para actualizar Mi Entidad"""
    
    def __init__(self, repository: MiRepository):
        self.repository = repository
    
    def execute(self, entidad_id: int, nueva_descripcion: str) -> MiEntidad:
        """Ejecutar caso de uso"""
        # Buscar entidad
        entidad = self.repository.find_by_id(entidad_id)
        if not entidad:
            raise MiEntidadNotFoundError(f"Entidad con ID {entidad_id} no encontrada")
        
        # Actualizar
        entidad.actualizar_descripcion(nueva_descripcion)
        
        # Guardar
        return self.repository.save(entidad)

class ObtenerMiEntidadUseCase:
    """Caso de uso para obtener Mi Entidad"""
    
    def __init__(self, repository: MiRepository):
        self.repository = repository
    
    def execute(self, entidad_id: int) -> MiEntidad:
        """Ejecutar caso de uso"""
        entidad = self.repository.find_by_id(entidad_id)
        if not entidad:
            raise MiEntidadNotFoundError(f"Entidad con ID {entidad_id} no encontrada")
        
        return entidad
```

### Excepciones de Dominio
```python
# modules/mi_modulo/domain/exception/mi_exceptions.py
class MiModuloError(Exception):
    """Excepción base para Mi Módulo"""
    pass

class MiEntidadNotFoundError(MiModuloError):
    """Excepción cuando no se encuentra la entidad"""
    pass

class MiEntidadAlreadyExistsError(MiModuloError):
    """Excepción cuando la entidad ya existe"""
    pass

class MiEntidadValidationError(MiModuloError):
    """Excepción de validación de entidad"""
    pass
```

## Paso 3: Implementar la Capa de Aplicación

### DTOs
```python
# modules/mi_modulo/application/dto/mi_dto.py
from dataclasses import dataclass
from typing import Optional
from datetime import datetime
from modules.mi_modulo.domain.entity.mi_entidad import MiEntidad

@dataclass
class MiEntidadDTO:
    """DTO para Mi Entidad"""
    id: Optional[int]
    nombre: str
    descripcion: str
    activo: bool
    created_at: datetime
    updated_at: datetime
    
    @classmethod
    def from_entity(cls, entidad: MiEntidad) -> 'MiEntidadDTO':
        """Crear DTO desde entidad"""
        return cls(
            id=entidad.id,
            nombre=entidad.nombre,
            descripcion=entidad.descripcion,
            activo=entidad.activo,
            created_at=entidad.created_at,
            updated_at=entidad.updated_at
        )

@dataclass
class CrearMiEntidadDTO:
    """DTO para crear Mi Entidad"""
    nombre: str
    descripcion: str

@dataclass
class ActualizarMiEntidadDTO:
    """DTO para actualizar Mi Entidad"""
    descripcion: str
```

### Servicio de Aplicación
```python
# modules/mi_modulo/application/service/mi_service.py
from typing import List, Optional
from modules.mi_modulo.domain.repository.mi_repository import MiRepository
from modules.mi_modulo.domain.usecase.mi_usecase import (
    CrearMiEntidadUseCase, ActualizarMiEntidadUseCase, ObtenerMiEntidadUseCase
)
from modules.mi_modulo.application.dto.mi_dto import (
    MiEntidadDTO, CrearMiEntidadDTO, ActualizarMiEntidadDTO
)
from shared.interfaces.events import event_bus, DomainEvent
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class MiService:
    """Servicio de aplicación para Mi Módulo"""
    
    def __init__(self, repository: MiRepository):
        self.repository = repository
        self.crear_usecase = CrearMiEntidadUseCase(repository)
        self.actualizar_usecase = ActualizarMiEntidadUseCase(repository)
        self.obtener_usecase = ObtenerMiEntidadUseCase(repository)
    
    async def crear_entidad(self, dto: CrearMiEntidadDTO) -> MiEntidadDTO:
        """Crear nueva entidad"""
        logger.info(f"Creando entidad: {dto.nombre}")
        
        # Ejecutar caso de uso
        entidad = self.crear_usecase.execute(dto.nombre, dto.descripcion)
        
        # Publicar evento
        event = DomainEvent(
            event_type="mi_entidad_created",
            data={
                "entidad_id": entidad.id,
                "nombre": entidad.nombre,
                "descripcion": entidad.descripcion
            },
            timestamp=datetime.now(),
            module_source="mi_modulo"
        )
        await event_bus.publish(event)
        
        logger.info(f"Entidad creada: {entidad.id}")
        return MiEntidadDTO.from_entity(entidad)
    
    async def actualizar_entidad(self, entidad_id: int, dto: ActualizarMiEntidadDTO) -> MiEntidadDTO:
        """Actualizar entidad existente"""
        logger.info(f"Actualizando entidad: {entidad_id}")
        
        # Ejecutar caso de uso
        entidad = self.actualizar_usecase.execute(entidad_id, dto.descripcion)
        
        # Publicar evento
        event = DomainEvent(
            event_type="mi_entidad_updated",
            data={
                "entidad_id": entidad.id,
                "nueva_descripcion": entidad.descripcion
            },
            timestamp=datetime.now(),
            module_source="mi_modulo"
        )
        await event_bus.publish(event)
        
        logger.info(f"Entidad actualizada: {entidad.id}")
        return MiEntidadDTO.from_entity(entidad)
    
    def obtener_entidad(self, entidad_id: int) -> MiEntidadDTO:
        """Obtener entidad por ID"""
        entidad = self.obtener_usecase.execute(entidad_id)
        return MiEntidadDTO.from_entity(entidad)
    
    def listar_entidades_activas(self) -> List[MiEntidadDTO]:
        """Listar todas las entidades activas"""
        entidades = self.repository.find_all_active()
        return [MiEntidadDTO.from_entity(e) for e in entidades]
    
    async def desactivar_entidad(self, entidad_id: int) -> MiEntidadDTO:
        """Desactivar entidad"""
        logger.info(f"Desactivando entidad: {entidad_id}")
        
        entidad = self.obtener_usecase.execute(entidad_id)
        entidad.desactivar()
        entidad_actualizada = self.repository.save(entidad)
        
        # Publicar evento
        event = DomainEvent(
            event_type="mi_entidad_deactivated",
            data={"entidad_id": entidad_id},
            timestamp=datetime.now(),
            module_source="mi_modulo"
        )
        await event_bus.publish(event)
        
        return MiEntidadDTO.from_entity(entidad_actualizada)
```

## Paso 4: Implementar Adaptadores

### Modelos de Base de Datos
```python
# modules/mi_modulo/adapter/output/persistence/sqlalchemy/models.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from modules.mi_modulo.domain.entity.mi_entidad import MiEntidad

Base = declarative_base()

class MiEntidadModel(Base):
    """Modelo SQLAlchemy para Mi Entidad"""
    __tablename__ = 'mi_entidades'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False, unique=True)
    descripcion = Column(Text)
    activo = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    @classmethod
    def from_entity(cls, entidad: MiEntidad) -> 'MiEntidadModel':
        """Crear modelo desde entidad"""
        return cls(
            id=entidad.id,
            nombre=entidad.nombre,
            descripcion=entidad.descripcion,
            activo=entidad.activo,
            created_at=entidad.created_at,
            updated_at=entidad.updated_at
        )
    
    def to_entity(self) -> MiEntidad:
        """Convertir modelo a entidad"""
        entidad = MiEntidad(self.nombre, self.descripcion)
        entidad.id = self.id
        entidad.activo = self.activo
        entidad.created_at = self.created_at
        entidad.updated_at = self.updated_at
        return entidad
    
    def update_from_entity(self, entidad: MiEntidad) -> None:
        """Actualizar modelo desde entidad"""
        self.nombre = entidad.nombre
        self.descripcion = entidad.descripcion
        self.activo = entidad.activo
        self.updated_at = entidad.updated_at
```

### Implementación del Repositorio
```python
# modules/mi_modulo/adapter/output/persistence/sqlalchemy/mi_repository.py
from sqlalchemy.orm import Session
from typing import List, Optional
from modules.mi_modulo.domain.repository.mi_repository import MiRepository
from modules.mi_modulo.domain.entity.mi_entidad import MiEntidad
from modules.mi_modulo.adapter.output.persistence.sqlalchemy.models import MiEntidadModel
from core.db.session import get_db_session

class MiSQLAlchemyRepository(MiRepository):
    """Implementación SQLAlchemy del repositorio"""
    
    def __init__(self):
        self.session: Session = get_db_session()
    
    def save(self, entidad: MiEntidad) -> MiEntidad:
        """Guardar entidad"""
        if entidad.id:
            # Actualizar existente
            model = self.session.query(MiEntidadModel).filter_by(id=entidad.id).first()
            if model:
                model.update_from_entity(entidad)
            else:
                model = MiEntidadModel.from_entity(entidad)
                self.session.add(model)
        else:
            # Crear nuevo
            model = MiEntidadModel.from_entity(entidad)
            self.session.add(model)
        
        self.session.commit()
        self.session.refresh(model)
        return model.to_entity()
    
    def find_by_id(self, entidad_id: int) -> Optional[MiEntidad]:
        """Buscar por ID"""
        model = self.session.query(MiEntidadModel).filter_by(id=entidad_id).first()
        return model.to_entity() if model else None
    
    def find_by_nombre(self, nombre: str) -> Optional[MiEntidad]:
        """Buscar por nombre"""
        model = self.session.query(MiEntidadModel).filter_by(nombre=nombre).first()
        return model.to_entity() if model else None
    
    def find_all_active(self) -> List[MiEntidad]:
        """Obtener todas las activas"""
        models = self.session.query(MiEntidadModel).filter_by(activo=True).all()
        return [model.to_entity() for model in models]
    
    def delete(self, entidad_id: int) -> bool:
        """Eliminar entidad"""
        model = self.session.query(MiEntidadModel).filter_by(id=entidad_id).first()
        if model:
            self.session.delete(model)
            self.session.commit()
            return True
        return False
    
    def exists_by_nombre(self, nombre: str) -> bool:
        """Verificar existencia por nombre"""
        count = self.session.query(MiEntidadModel).filter_by(nombre=nombre).count()
        return count > 0
```

### Adaptador del Repositorio
```python
# modules/mi_modulo/adapter/output/persistence/repository_adapter.py
from modules.mi_modulo.domain.repository.mi_repository import MiRepository
from modules.mi_modulo.adapter.output.persistence.sqlalchemy.mi_repository import MiSQLAlchemyRepository

class MiRepositoryAdapter:
    """Adaptador del repositorio"""
    
    def __init__(self, repository: MiSQLAlchemyRepository):
        self._repository = repository
    
    def __getattr__(self, name):
        """Delegar llamadas al repositorio subyacente"""
        return getattr(self._repository, name)
```

### Request/Response Models
```python
# modules/mi_modulo/adapter/input/api/v1/request/mi_request.py
from pydantic import BaseModel, Field
from typing import Optional

class CrearMiEntidadRequest(BaseModel):
    """Request para crear Mi Entidad"""
    nombre: str = Field(..., min_length=1, max_length=100, description="Nombre de la entidad")
    descripcion: str = Field("", max_length=500, description="Descripción de la entidad")

class ActualizarMiEntidadRequest(BaseModel):
    """Request para actualizar Mi Entidad"""
    descripcion: str = Field(..., max_length=500, description="Nueva descripción")

# modules/mi_modulo/adapter/input/api/v1/response/mi_response.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from modules.mi_modulo.application.dto.mi_dto import MiEntidadDTO

class MiEntidadResponse(BaseModel):
    """Response para Mi Entidad"""
    id: int
    nombre: str
    descripcion: str
    activo: bool
    created_at: datetime
    updated_at: datetime
    
    @classmethod
    def from_dto(cls, dto: MiEntidadDTO) -> 'MiEntidadResponse':
        return cls(
            id=dto.id,
            nombre=dto.nombre,
            descripcion=dto.descripcion,
            activo=dto.activo,
            created_at=dto.created_at,
            updated_at=dto.updated_at
        )

class CrearMiEntidadResponse(BaseModel):
    """Response para creación exitosa"""
    message: str = "Entidad creada exitosamente"
    entidad: MiEntidadResponse
```

### Controlador API
```python
# modules/mi_modulo/adapter/input/api/v1/mi_controller.py
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from modules.mi_modulo.application.service.mi_service import MiService
from modules.mi_modulo.adapter.input.api.v1.request.mi_request import (
    CrearMiEntidadRequest, ActualizarMiEntidadRequest
)
from modules.mi_modulo.adapter.input.api.v1.response.mi_response import (
    MiEntidadResponse, CrearMiEntidadResponse
)
from modules.mi_modulo.application.dto.mi_dto import CrearMiEntidadDTO, ActualizarMiEntidadDTO
from modules.mi_modulo.domain.exception.mi_exceptions import (
    MiEntidadNotFoundError, MiEntidadAlreadyExistsError
)
from shared.decorators.permission import require_permission
from modules.auth.adapter.input.api.dependencies import get_current_user

router = APIRouter(prefix="/mi-modulo", tags=["Mi Módulo"])

@router.post("/entidades", response_model=CrearMiEntidadResponse, status_code=status.HTTP_201_CREATED)
@require_permission("mi_modulo", "create")
async def crear_entidad(
    request: CrearMiEntidadRequest,
    mi_service: MiService = Depends(),
    current_user = Depends(get_current_user)
):
    """Crear nueva entidad"""
    try:
        dto = CrearMiEntidadDTO(nombre=request.nombre, descripcion=request.descripcion)
        entidad_dto = await mi_service.crear_entidad(dto)
        
        return CrearMiEntidadResponse(
            entidad=MiEntidadResponse.from_dto(entidad_dto)
        )
    except MiEntidadAlreadyExistsError as e:
        raise HTTPException(status_code=409, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")

@router.get("/entidades", response_model=List[MiEntidadResponse])
@require_permission("mi_modulo", "read")
async def listar_entidades(
    mi_service: MiService = Depends(),
    current_user = Depends(get_current_user)
):
    """Listar todas las entidades activas"""
    entidades_dto = mi_service.listar_entidades_activas()
    return [MiEntidadResponse.from_dto(dto) for dto in entidades_dto]

@router.get("/entidades/{entidad_id}", response_model=MiEntidadResponse)
@require_permission("mi_modulo", "read")
async def obtener_entidad(
    entidad_id: int,
    mi_service: MiService = Depends(),
    current_user = Depends(get_current_user)
):
    """Obtener entidad por ID"""
    try:
        entidad_dto = mi_service.obtener_entidad(entidad_id)
        return MiEntidadResponse.from_dto(entidad_dto)
    except MiEntidadNotFoundError:
        raise HTTPException(status_code=404, detail="Entidad no encontrada")

@router.put("/entidades/{entidad_id}", response_model=MiEntidadResponse)
@require_permission("mi_modulo", "update")
async def actualizar_entidad(
    entidad_id: int,
    request: ActualizarMiEntidadRequest,
    mi_service: MiService = Depends(),
    current_user = Depends(get_current_user)
):
    """Actualizar entidad"""
    try:
        dto = ActualizarMiEntidadDTO(descripcion=request.descripcion)
        entidad_dto = await mi_service.actualizar_entidad(entidad_id, dto)
        return MiEntidadResponse.from_dto(entidad_dto)
    except MiEntidadNotFoundError:
        raise HTTPException(status_code=404, detail="Entidad no encontrada")

@router.delete("/entidades/{entidad_id}", status_code=status.HTTP_204_NO_CONTENT)
@require_permission("mi_modulo", "delete")
async def desactivar_entidad(
    entidad_id: int,
    mi_service: MiService = Depends(),
    current_user = Depends(get_current_user)
):
    """Desactivar entidad"""
    try:
        await mi_service.desactivar_entidad(entidad_id)
    except MiEntidadNotFoundError:
        raise HTTPException(status_code=404, detail="Entidad no encontrada")
```

## Paso 5: Configuración del Módulo

### Container de Dependencias
```python
# modules/mi_modulo/container.py
from dependency_injector.providers import Factory, Singleton
from dependency_injector.containers import DeclarativeContainer, WiringConfiguration

from modules.mi_modulo.adapter.output.persistence.repository_adapter import MiRepositoryAdapter
from modules.mi_modulo.adapter.output.persistence.sqlalchemy.mi_repository import MiSQLAlchemyRepository
from modules.mi_modulo.application.service.mi_service import MiService

class MiModuloContainer(DeclarativeContainer):
    """Container de dependencias para Mi Módulo"""
    wiring_config = WiringConfiguration(packages=["modules.mi_modulo"], auto_wire=True)

    # Repositorio
    repository = Singleton(MiSQLAlchemyRepository)

    # Adaptador del repositorio
    repository_adapter = Factory(
        MiRepositoryAdapter,
        repository=repository
    )

    # Servicio de aplicación
    service = Factory(
        MiService,
        repository=repository_adapter
    )
```

### Definición del Módulo
```python
# modules/mi_modulo/module.py
from fastapi import APIRouter
from dependency_injector.containers import DeclarativeContainer
import os
import logging

from shared.interfaces.module_registry import ModuleInterface
from modules.mi_modulo.container import MiModuloContainer
from core.fastapi.server.route_helpers import get_routes, set_routes_to_app
from shared.interfaces.service_locator import service_locator
from shared.interfaces.events import event_bus

logger = logging.getLogger(__name__)

class MiModuloModule(ModuleInterface):
    """Módulo Mi Módulo con auto-registro"""
    
    def __init__(self):
        self._container = None
        self._routes = None
        self._initialized = False
    
    @property
    def name(self) -> str:
        return "mi_modulo"
    
    @property
    def version(self) -> str:
        return "1.0.0"
    
    @property
    def dependencies(self) -> list[str]:
        return ["auth", "rbac"]  # Dependencias del módulo
    
    @property
    def enabled(self) -> bool:
        return os.getenv("MI_MODULO_ENABLED", "true").lower() == "true"
    
    @property
    def container(self) -> DeclarativeContainer:
        if not self._container:
            self._container = MiModuloContainer()
        return self._container
    
    @property
    def routes(self) -> APIRouter:
        if not self._routes:
            self._routes = self._setup_routes()
        return self._routes
    
    def initialize(self) -> None:
        """Inicialización del módulo"""
        if self._initialized:
            return
        
        logger.info(f"Initializing {self.name} module...")
        
        # Configurar container
        self.container.wire(modules=[f"modules.{self.name}"])
        
        # Registrar servicios en el service locator
        service_locator.register_service("mi_modulo_service", self.container.service())
        
        # Suscribirse a eventos (si es necesario)
        # event_bus.subscribe("some_event", self._handle_some_event)
        
        self._initialized = True
        logger.info(f"✅ {self.name} module initialized")
    
    def shutdown(self) -> None:
        """Limpieza del módulo"""
        if not self._initialized:
            return
        
        logger.info(f"Shutting down {self.name} module...")
        
        # Limpiar recursos si es necesario
        
        self._initialized = False
        logger.info(f"✅ {self.name} module shutdown")
    
    def _setup_routes(self) -> APIRouter:
        """Configurar rutas del módulo"""
        routes = get_routes(f"modules.{self.name}")
        router = APIRouter(prefix="/mi-modulo", tags=["Mi Módulo"])
        set_routes_to_app(router, routes)
        return router
```

## Paso 6: Migración de Base de Datos

### Crear Migración
```python
# migrations/versions/xxx_create_mi_entidades_table.py
"""Create mi_entidades table

Revision ID: xxx
Revises: previous_revision
Create Date: 2024-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = 'xxx'
down_revision = 'previous_revision'
branch_labels = None
depends_on = None

def upgrade():
    # Crear tabla mi_entidades
    op.create_table('mi_entidades',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('nombre', sa.String(length=100), nullable=False),
        sa.Column('descripcion', sa.Text(), nullable=True),
        sa.Column('activo', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('nombre')
    )

def downgrade():
    op.drop_table('mi_entidades')
```

## Paso 7: Tests

### Tests Unitarios
```python
# tests/unit/mi_modulo/test_mi_service.py
import pytest
from unittest.mock import Mock
from modules.mi_modulo.application.service.mi_service import MiService
from modules.mi_modulo.application.dto.mi_dto import CrearMiEntidadDTO
from modules.mi_modulo.domain.entity.mi_entidad import MiEntidad

class TestMiService:
    def test_crear_entidad_success(self):
        # Arrange
        mock_repository = Mock()
        mock_repository.exists_by_nombre.return_value = False
        mock_repository.save.return_value = MiEntidad("Test", "Descripción test")
        
        service = MiService(mock_repository)
        dto = CrearMiEntidadDTO(nombre="Test", descripcion="Descripción test")
        
        # Act
        result = service.crear_entidad(dto)
        
        # Assert
        assert result.nombre == "Test"
        mock_repository.save.assert_called_once()
```

### Tests de Integración
```python
# tests/integration/mi_modulo/test_mi_endpoints.py
import pytest
from fastapi.testclient import TestClient

class TestMiModuloEndpoints:
    def test_crear_entidad_success(self, client: TestClient, admin_token):
        # Arrange
        headers = {"Authorization": f"Bearer {admin_token}"}
        data = {"nombre": "Test Entity", "descripcion": "Test description"}
        
        # Act
        response = client.post("/mi-modulo/entidades", json=data, headers=headers)
        
        # Assert
        assert response.status_code == 201
        assert response.json()["entidad"]["nombre"] == "Test Entity"
```

## Paso 8: Documentación

### README del Módulo
```markdown
# Mi Módulo

## Descripción
Módulo para gestión de [descripción de la funcionalidad].

## Funcionalidades
- Crear entidades
- Actualizar entidades
- Listar entidades activas
- Desactivar entidades

## Endpoints
- `POST /mi-modulo/entidades` - Crear entidad
- `GET /mi-modulo/entidades` - Listar entidades
- `GET /mi-modulo/entidades/{id}` - Obtener entidad
- `PUT /mi-modulo/entidades/{id}` - Actualizar entidad
- `DELETE /mi-modulo/entidades/{id}` - Desactivar entidad

## Permisos Requeridos
- `mi_modulo:create` - Crear entidades
- `mi_modulo:read` - Leer entidades
- `mi_modulo:update` - Actualizar entidades
- `mi_modulo:delete` - Desactivar entidades

## Eventos Publicados
- `mi_entidad_created` - Cuando se crea una entidad
- `mi_entidad_updated` - Cuando se actualiza una entidad
- `mi_entidad_deactivated` - Cuando se desactiva una entidad

## Configuración
- `MI_MODULO_ENABLED` - Habilitar/deshabilitar módulo (default: true)
```

## Paso 9: Registro Automático

El módulo se registrará automáticamente al estar en la carpeta `modules/` y seguir la estructura correcta. No se requiere configuración adicional.

### Verificar Registro
```bash
# Ejecutar aplicación
python main.py

# Verificar que el módulo está registrado
curl http://localhost:8000/health
```

## Mejores Prácticas

### 1. **Naming Conventions**
- Usar nombres descriptivos y consistentes
- Seguir convenciones de Python (snake_case)
- Prefijos claros para evitar conflictos

### 2. **Error Handling**
- Excepciones específicas por capa
- Logging apropiado
- Respuestas HTTP consistentes

### 3. **Testing**
- Tests unitarios para lógica de dominio
- Tests de integración para endpoints
- Mocks para dependencias externas

### 4. **Documentation**
- Docstrings en todas las clases y métodos
- README específico del módulo
- Ejemplos de uso

### 5. **Performance**
- Lazy loading de dependencias
- Paginación en listados
- Índices apropiados en base de datos

Con esta guía, puedes crear módulos completamente funcionales que se integran automáticamente en el sistema siguiendo la arquitectura hexagonal desacoplada.