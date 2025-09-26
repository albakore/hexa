# Implementación del Sistema RBAC

## Arquitectura de Implementación

El sistema RBAC está implementado siguiendo la arquitectura hexagonal, con separación clara entre dominio, aplicación y adaptadores.

## Estructura del Módulo RBAC

```
modules/rbac/
├── domain/
│   ├── entity/
│   │   ├── role.py
│   │   ├── permission.py
│   │   └── user_role.py
│   ├── repository/
│   │   ├── rbac.py
│   │   ├── role.py
│   │   └── permission.py
│   ├── usecase/
│   │   ├── role.py
│   │   └── permission.py
│   └── exception/
│       └── rbac_exceptions.py
├── application/
│   └── service/
│       ├── role.py
│       └── permission.py
├── adapter/
│   ├── input/
│   │   └── api/v1/rbac.py
│   └── output/
│       └── persistence/
│           ├── sqlalchemy/rbac.py
│           └── repository_adapter.py
├── container.py
└── module.py
```

## Implementación de Repositorios

### Interface del Repositorio
```python
# modules/rbac/domain/repository/rbac.py
from abc import ABC, abstractmethod
from typing import List, Optional
from modules.rbac.domain.entity.role import Role
from modules.rbac.domain.entity.permission import Permission

class RBACRepository(ABC):
    """Interface del repositorio RBAC"""
    
    # Métodos de Role
    @abstractmethod
    def save_role(self, role: Role) -> Role:
        pass
    
    @abstractmethod
    def find_role_by_id(self, role_id: int) -> Optional[Role]:
        pass
    
    @abstractmethod
    def find_role_by_name(self, name: str) -> Optional[Role]:
        pass
    
    @abstractmethod
    def get_all_roles(self) -> List[Role]:
        pass
    
    # Métodos de Permission
    @abstractmethod
    def save_permission(self, permission: Permission) -> Permission:
        pass
    
    @abstractmethod
    def find_permission_by_id(self, permission_id: int) -> Optional[Permission]:
        pass
    
    @abstractmethod
    def find_permission_by_name(self, name: str) -> Optional[Permission]:
        pass
    
    @abstractmethod
    def get_all_permissions(self) -> List[Permission]:
        pass
    
    # Métodos de User-Role
    @abstractmethod
    def assign_role_to_user(self, user_id: int, role_id: int) -> None:
        pass
    
    @abstractmethod
    def remove_role_from_user(self, user_id: int, role_id: int) -> None:
        pass
    
    @abstractmethod
    def get_user_roles(self, user_id: int) -> List[Role]:
        pass
    
    @abstractmethod
    def get_role_users(self, role_id: int) -> List[int]:
        pass
    
    # Métodos de Role-Permission
    @abstractmethod
    def assign_permission_to_role(self, role_id: int, permission_id: int) -> None:
        pass
    
    @abstractmethod
    def remove_permission_from_role(self, role_id: int, permission_id: int) -> None:
        pass
    
    @abstractmethod
    def get_role_permissions(self, role_id: int) -> List[Permission]:
        pass
```

### Implementación SQLAlchemy
```python
# modules/rbac/adapter/output/persistence/sqlalchemy/rbac.py
from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import List, Optional

from modules.rbac.domain.repository.rbac import RBACRepository
from modules.rbac.domain.entity.role import Role
from modules.rbac.domain.entity.permission import Permission
from core.db.session import get_db_session

class RBACSQLAlchemyRepository(RBACRepository):
    def __init__(self):
        self.session: Session = get_db_session()
    
    # Implementación de métodos de Role
    def save_role(self, role: Role) -> Role:
        role_model = RoleModel.from_entity(role)
        
        if role.id:
            # Actualizar
            existing = self.session.query(RoleModel).filter_by(id=role.id).first()
            if existing:
                existing.name = role_model.name
                existing.description = role_model.description
                existing.is_active = role_model.is_active
                role_model = existing
        else:
            # Crear nuevo
            self.session.add(role_model)
        
        self.session.commit()
        self.session.refresh(role_model)
        return role_model.to_entity()
    
    def find_role_by_id(self, role_id: int) -> Optional[Role]:
        role_model = self.session.query(RoleModel).filter_by(id=role_id).first()
        return role_model.to_entity() if role_model else None
    
    def find_role_by_name(self, name: str) -> Optional[Role]:
        role_model = self.session.query(RoleModel).filter_by(name=name).first()
        return role_model.to_entity() if role_model else None
    
    def get_all_roles(self) -> List[Role]:
        role_models = self.session.query(RoleModel).filter_by(is_active=True).all()
        return [model.to_entity() for model in role_models]
    
    # Implementación de métodos de Permission
    def save_permission(self, permission: Permission) -> Permission:
        perm_model = PermissionModel.from_entity(permission)
        
        if permission.id:
            existing = self.session.query(PermissionModel).filter_by(id=permission.id).first()
            if existing:
                existing.name = perm_model.name
                existing.resource = perm_model.resource
                existing.action = perm_model.action
                existing.description = perm_model.description
                existing.is_active = perm_model.is_active
                perm_model = existing
        else:
            self.session.add(perm_model)
        
        self.session.commit()
        self.session.refresh(perm_model)
        return perm_model.to_entity()
    
    def find_permission_by_id(self, permission_id: int) -> Optional[Permission]:
        perm_model = self.session.query(PermissionModel).filter_by(id=permission_id).first()
        return perm_model.to_entity() if perm_model else None
    
    def find_permission_by_name(self, name: str) -> Optional[Permission]:
        perm_model = self.session.query(PermissionModel).filter_by(name=name).first()
        return perm_model.to_entity() if perm_model else None
    
    # Implementación de relaciones User-Role
    def assign_role_to_user(self, user_id: int, role_id: int) -> None:
        # Verificar si ya existe la relación
        existing = self.session.query(UserRoleModel).filter(
            and_(UserRoleModel.user_id == user_id, UserRoleModel.role_id == role_id)
        ).first()
        
        if not existing:
            user_role = UserRoleModel(user_id=user_id, role_id=role_id)
            self.session.add(user_role)
            self.session.commit()
    
    def remove_role_from_user(self, user_id: int, role_id: int) -> None:
        user_role = self.session.query(UserRoleModel).filter(
            and_(UserRoleModel.user_id == user_id, UserRoleModel.role_id == role_id)
        ).first()
        
        if user_role:
            self.session.delete(user_role)
            self.session.commit()
    
    def get_user_roles(self, user_id: int) -> List[Role]:
        role_models = self.session.query(RoleModel).join(UserRoleModel).filter(
            and_(UserRoleModel.user_id == user_id, RoleModel.is_active == True)
        ).all()
        
        roles = []
        for role_model in role_models:
            role = role_model.to_entity()
            # Cargar permisos del rol
            role.permissions = self.get_role_permissions(role.id)
            roles.append(role)
        
        return roles
    
    # Implementación de relaciones Role-Permission
    def assign_permission_to_role(self, role_id: int, permission_id: int) -> None:
        existing = self.session.query(RolePermissionModel).filter(
            and_(RolePermissionModel.role_id == role_id, 
                 RolePermissionModel.permission_id == permission_id)
        ).first()
        
        if not existing:
            role_permission = RolePermissionModel(role_id=role_id, permission_id=permission_id)
            self.session.add(role_permission)
            self.session.commit()
    
    def get_role_permissions(self, role_id: int) -> List[Permission]:
        perm_models = self.session.query(PermissionModel).join(RolePermissionModel).filter(
            and_(RolePermissionModel.role_id == role_id, PermissionModel.is_active == True)
        ).all()
        
        return [model.to_entity() for model in perm_models]
```

## Modelos de Base de Datos

### Modelos SQLAlchemy
```python
# modules/rbac/adapter/output/persistence/sqlalchemy/models.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

# Tabla de asociación User-Role
user_role_table = Table(
    'user_roles',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('role_id', Integer, ForeignKey('roles.id'), primary_key=True),
    Column('assigned_at', DateTime, default=datetime.now)
)

# Tabla de asociación Role-Permission
role_permission_table = Table(
    'role_permissions',
    Base.metadata,
    Column('role_id', Integer, ForeignKey('roles.id'), primary_key=True),
    Column('permission_id', Integer, ForeignKey('permissions.id'), primary_key=True),
    Column('assigned_at', DateTime, default=datetime.now)
)

class RoleModel(Base):
    __tablename__ = 'roles'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(String(255))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # Relaciones
    permissions = relationship("PermissionModel", secondary=role_permission_table, back_populates="roles")
    
    @classmethod
    def from_entity(cls, role: Role) -> 'RoleModel':
        return cls(
            id=role.id,
            name=role.name,
            description=role.description,
            is_active=role.is_active,
            created_at=role.created_at
        )
    
    def to_entity(self) -> Role:
        role = Role(self.name, self.description)
        role.id = self.id
        role.is_active = self.is_active
        role.created_at = self.created_at
        return role

class PermissionModel(Base):
    __tablename__ = 'permissions'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False)
    resource = Column(String(50), nullable=False)
    action = Column(String(50), nullable=False)
    description = Column(String(255))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)
    
    # Relaciones
    roles = relationship("RoleModel", secondary=role_permission_table, back_populates="permissions")
    
    @classmethod
    def from_entity(cls, permission: Permission) -> 'PermissionModel':
        return cls(
            id=permission.id,
            name=permission.name,
            resource=permission.resource,
            action=permission.action,
            description=permission.description,
            is_active=permission.is_active,
            created_at=permission.created_at
        )
    
    def to_entity(self) -> Permission:
        permission = Permission(self.name, self.resource, self.action, self.description)
        permission.id = self.id
        permission.is_active = self.is_active
        permission.created_at = self.created_at
        return permission
```

## DTOs y Serialización

### DTOs de RBAC
```python
# modules/rbac/application/dto/rbac_dto.py
from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime

@dataclass
class RoleDTO:
    id: Optional[int]
    name: str
    description: str
    is_active: bool
    created_at: datetime
    permissions: List['PermissionDTO'] = None
    
    @classmethod
    def from_entity(cls, role: Role) -> 'RoleDTO':
        return cls(
            id=role.id,
            name=role.name,
            description=role.description,
            is_active=role.is_active,
            created_at=role.created_at,
            permissions=[PermissionDTO.from_entity(p) for p in role.permissions] if role.permissions else []
        )

@dataclass
class PermissionDTO:
    id: Optional[int]
    name: str
    resource: str
    action: str
    description: str
    is_active: bool
    created_at: datetime
    
    @classmethod
    def from_entity(cls, permission: Permission) -> 'PermissionDTO':
        return cls(
            id=permission.id,
            name=permission.name,
            resource=permission.resource,
            action=permission.action,
            description=permission.description,
            is_active=permission.is_active,
            created_at=permission.created_at
        )

@dataclass
class UserRoleDTO:
    user_id: int
    roles: List[RoleDTO]
    
    @classmethod
    def from_user_roles(cls, user_id: int, roles: List[Role]) -> 'UserRoleDTO':
        return cls(
            user_id=user_id,
            roles=[RoleDTO.from_entity(role) for role in roles]
        )
```

## Requests y Responses

### Request Models
```python
# modules/rbac/adapter/input/api/v1/request/rbac_request.py
from pydantic import BaseModel, Field
from typing import Optional

class CreateRoleRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=50, description="Nombre del rol")
    description: str = Field("", max_length=255, description="Descripción del rol")

class UpdateRoleRequest(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=50)
    description: Optional[str] = Field(None, max_length=255)
    is_active: Optional[bool] = None

class CreatePermissionRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Nombre del permiso")
    resource: str = Field(..., min_length=1, max_length=50, description="Recurso")
    action: str = Field(..., min_length=1, max_length=50, description="Acción")
    description: str = Field("", max_length=255, description="Descripción del permiso")

class AssignRoleRequest(BaseModel):
    user_id: int = Field(..., gt=0, description="ID del usuario")
    role_id: int = Field(..., gt=0, description="ID del rol")

class CheckPermissionRequest(BaseModel):
    user_id: int = Field(..., gt=0, description="ID del usuario")
    resource: str = Field(..., min_length=1, description="Recurso")
    action: str = Field(..., min_length=1, description="Acción")
```

### Response Models
```python
# modules/rbac/adapter/input/api/v1/response/rbac_response.py
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class PermissionResponse(BaseModel):
    id: int
    name: str
    resource: str
    action: str
    description: str
    is_active: bool
    created_at: datetime
    
    @classmethod
    def from_dto(cls, dto: PermissionDTO) -> 'PermissionResponse':
        return cls(
            id=dto.id,
            name=dto.name,
            resource=dto.resource,
            action=dto.action,
            description=dto.description,
            is_active=dto.is_active,
            created_at=dto.created_at
        )

class RoleResponse(BaseModel):
    id: int
    name: str
    description: str
    is_active: bool
    created_at: datetime
    permissions: List[PermissionResponse] = []
    
    @classmethod
    def from_dto(cls, dto: RoleDTO) -> 'RoleResponse':
        return cls(
            id=dto.id,
            name=dto.name,
            description=dto.description,
            is_active=dto.is_active,
            created_at=dto.created_at,
            permissions=[PermissionResponse.from_dto(p) for p in dto.permissions] if dto.permissions else []
        )

class UserRolesResponse(BaseModel):
    user_id: int
    roles: List[RoleResponse]
    
    @classmethod
    def from_dto(cls, dto: UserRoleDTO) -> 'UserRolesResponse':
        return cls(
            user_id=dto.user_id,
            roles=[RoleResponse.from_dto(role) for role in dto.roles]
        )

class CheckPermissionResponse(BaseModel):
    has_permission: bool
    user_id: int
    resource: str
    action: str
```

## Controladores API

### RBAC Controller
```python
# modules/rbac/adapter/input/api/v1/rbac.py
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from modules.rbac.application.service.role import RoleService
from modules.rbac.application.service.permission import PermissionService
from modules.rbac.adapter.input.api.v1.request.rbac_request import *
from modules.rbac.adapter.input.api.v1.response.rbac_response import *
from modules.auth.adapter.input.api.dependencies import get_current_user
from shared.decorators.permission import require_permission

router = APIRouter(prefix="/rbac", tags=["RBAC"])

# Endpoints de Roles
@router.post("/roles", response_model=RoleResponse, status_code=status.HTTP_201_CREATED)
@require_permission("rbac", "create_role")
async def create_role(
    request: CreateRoleRequest,
    role_service: RoleService = Depends(),
    current_user = Depends(get_current_user)
):
    """Crear nuevo rol"""
    role_dto = role_service.create_role(request.name, request.description)
    return RoleResponse.from_dto(role_dto)

@router.get("/roles", response_model=List[RoleResponse])
@require_permission("rbac", "view_roles")
async def get_roles(
    role_service: RoleService = Depends(),
    current_user = Depends(get_current_user)
):
    """Obtener todos los roles"""
    roles = role_service.get_all_roles()
    return [RoleResponse.from_dto(role) for role in roles]

@router.get("/roles/{role_id}", response_model=RoleResponse)
@require_permission("rbac", "view_roles")
async def get_role(
    role_id: int,
    role_service: RoleService = Depends(),
    current_user = Depends(get_current_user)
):
    """Obtener rol por ID"""
    role = role_service.get_role_by_id(role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return RoleResponse.from_dto(role)

# Endpoints de Permisos
@router.post("/permissions", response_model=PermissionResponse, status_code=status.HTTP_201_CREATED)
@require_permission("rbac", "create_permission")
async def create_permission(
    request: CreatePermissionRequest,
    permission_service: PermissionService = Depends(),
    current_user = Depends(get_current_user)
):
    """Crear nuevo permiso"""
    permission_dto = permission_service.create_permission(
        request.name, request.resource, request.action, request.description
    )
    return PermissionResponse.from_dto(permission_dto)

@router.get("/permissions", response_model=List[PermissionResponse])
@require_permission("rbac", "view_permissions")
async def get_permissions(
    permission_service: PermissionService = Depends(),
    current_user = Depends(get_current_user)
):
    """Obtener todos los permisos"""
    permissions = permission_service.get_all_permissions()
    return [PermissionResponse.from_dto(perm) for perm in permissions]

# Endpoints de Asignación
@router.post("/users/{user_id}/roles/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
@require_permission("rbac", "assign_role")
async def assign_role_to_user(
    user_id: int,
    role_id: int,
    role_service: RoleService = Depends(),
    current_user = Depends(get_current_user)
):
    """Asignar rol a usuario"""
    role_service.assign_role_to_user(user_id, role_id)

@router.get("/users/{user_id}/roles", response_model=UserRolesResponse)
@require_permission("rbac", "view_roles")
async def get_user_roles(
    user_id: int,
    role_service: RoleService = Depends(),
    current_user = Depends(get_current_user)
):
    """Obtener roles de un usuario"""
    user_roles = role_service.get_user_roles_dto(user_id)
    return UserRolesResponse.from_dto(user_roles)

@router.post("/permissions/check", response_model=CheckPermissionResponse)
async def check_permission(
    request: CheckPermissionRequest,
    permission_service: PermissionService = Depends(),
    current_user = Depends(get_current_user)
):
    """Verificar permiso de usuario"""
    has_permission = permission_service.check_user_permission(
        request.user_id, request.resource, request.action
    )
    return CheckPermissionResponse(
        has_permission=has_permission,
        user_id=request.user_id,
        resource=request.resource,
        action=request.action
    )
```

## Migraciones de Base de Datos

### Migración Inicial
```python
# migrations/versions/001_create_rbac_tables.py
"""Create RBAC tables

Revision ID: 001
Revises: 
Create Date: 2024-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers
revision = '001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Crear tabla roles
    op.create_table('roles',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('name', sa.String(length=50), nullable=False),
        sa.Column('description', sa.String(length=255), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )
    
    # Crear tabla permissions
    op.create_table('permissions',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('resource', sa.String(length=50), nullable=False),
        sa.Column('action', sa.String(length=50), nullable=False),
        sa.Column('description', sa.String(length=255), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )
    
    # Crear tabla user_roles
    op.create_table('user_roles',
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('role_id', sa.Integer(), nullable=False),
        sa.Column('assigned_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('user_id', 'role_id')
    )
    
    # Crear tabla role_permissions
    op.create_table('role_permissions',
        sa.Column('role_id', sa.Integer(), nullable=False),
        sa.Column('permission_id', sa.Integer(), nullable=False),
        sa.Column('assigned_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['permission_id'], ['permissions.id'], ),
        sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ),
        sa.PrimaryKeyConstraint('role_id', 'permission_id')
    )

def downgrade():
    op.drop_table('role_permissions')
    op.drop_table('user_roles')
    op.drop_table('permissions')
    op.drop_table('roles')
```

## Configuración del Container

### RBAC Container
```python
# modules/rbac/container.py
from dependency_injector.providers import Factory, Singleton
from dependency_injector.containers import DeclarativeContainer, WiringConfiguration

from modules.rbac.adapter.output.persistence.repository_adapter import RBACRepositoryAdapter
from modules.rbac.adapter.output.persistence.sqlalchemy.rbac import RBACSQLAlchemyRepository
from modules.rbac.application.service.role import RoleService
from modules.rbac.application.service.permission import PermissionService

class RBACContainer(DeclarativeContainer):
    wiring_config = WiringConfiguration(packages=["modules.rbac"], auto_wire=True)

    repository = Singleton(RBACSQLAlchemyRepository)

    repository_adapter = Factory(
        RBACRepositoryAdapter,
        role_repository=repository,
        permission_repository=repository,
    )

    role_service = Factory(
        RoleService,
        repository=repository_adapter,
    )

    permission_service = Factory(
        PermissionService,
        repository=repository_adapter
    )
```

## Inicialización del Sistema

### Script de Inicialización
```python
# scripts/init_rbac.py
"""Script para inicializar el sistema RBAC con datos por defecto"""

from modules.rbac.application.service.role import RoleService
from modules.rbac.application.service.permission import PermissionService
from modules.rbac.domain.entity.system_roles import SystemRoles
from modules.rbac.domain.entity.system_permissions import SystemPermissions
from shared.interfaces.service_locator import service_locator

def initialize_rbac_system():
    """Inicializar sistema RBAC completo"""
    print("🔧 Initializing RBAC system...")
    
    # Inicializar permisos
    initialize_permissions()
    
    # Inicializar roles
    initialize_roles()
    
    # Asignar permisos a roles
    assign_permissions_to_roles()
    
    print("✅ RBAC system initialized successfully!")

def initialize_permissions():
    """Inicializar permisos del sistema"""
    permission_service = service_locator.get_service("permission_service")
    
    for perm_data in SystemPermissions.get_all_permissions():
        try:
            permission_service.create_permission(
                name=perm_data["name"],
                resource=perm_data["resource"],
                action=perm_data["action"],
                description=perm_data["description"]
            )
            print(f"  ✅ Permission: {perm_data['name']}")
        except Exception as e:
            print(f"  ⚠️  Permission exists: {perm_data['name']}")

def initialize_roles():
    """Inicializar roles del sistema"""
    role_service = service_locator.get_service("role_service")
    
    for role_data in SystemRoles.get_default_roles():
        try:
            role_service.create_role(
                name=role_data["name"],
                description=role_data["description"]
            )
            print(f"  ✅ Role: {role_data['name']}")
        except Exception as e:
            print(f"  ⚠️  Role exists: {role_data['name']}")

def assign_permissions_to_roles():
    """Asignar permisos por defecto a roles"""
    role_service = service_locator.get_service("role_service")
    
    # Super Admin: todos los permisos
    super_admin_permissions = SystemPermissions.get_all_permissions()
    for perm in super_admin_permissions:
        try:
            role_service.assign_permission_to_role_by_name(
                SystemRoles.SUPER_ADMIN, perm["name"]
            )
        except Exception:
            pass
    
    # Admin: permisos básicos de administración
    admin_permissions = [
        SystemPermissions.USER_CREATE,
        SystemPermissions.USER_READ,
        SystemPermissions.USER_UPDATE,
        SystemPermissions.RBAC_VIEW_ROLES,
        SystemPermissions.RBAC_ASSIGN_ROLE,
    ]
    for perm in admin_permissions:
        try:
            role_service.assign_permission_to_role_by_name(
                SystemRoles.ADMIN, perm
            )
        except Exception:
            pass
    
    print("  ✅ Permissions assigned to roles")

if __name__ == "__main__":
    initialize_rbac_system()
```

Este sistema RBAC proporciona una base sólida y extensible para el control de acceso en la aplicación, siguiendo los principios de la arquitectura hexagonal y manteniendo la separación de responsabilidades.