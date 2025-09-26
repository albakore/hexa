# Sistema de Roles

## Definición de RBAC

El sistema implementa **Role-Based Access Control (RBAC)**, un modelo de seguridad que controla el acceso a recursos basándose en los roles asignados a los usuarios.

## Arquitectura del Sistema de Roles

### Componentes Principales

```
User ←→ UserRole ←→ Role ←→ RolePermission ←→ Permission
```

- **User**: Usuario del sistema
- **Role**: Rol que agrupa permisos
- **Permission**: Permiso específico sobre un recurso
- **UserRole**: Relación usuario-rol (muchos a muchos)
- **RolePermission**: Relación rol-permiso (muchos a muchos)

## Entidades de Dominio

### Role Entity
```python
# modules/rbac/domain/entity/role.py
class Role:
    def __init__(self, name: str, description: str):
        self.name = self._validate_name(name)
        self.description = description
        self.is_active = True
        self.permissions: List[Permission] = []
        self.created_at = datetime.now()
    
    def add_permission(self, permission: Permission) -> None:
        """Agregar permiso al rol"""
        if permission not in self.permissions:
            self.permissions.append(permission)
    
    def remove_permission(self, permission: Permission) -> None:
        """Remover permiso del rol"""
        if permission in self.permissions:
            self.permissions.remove(permission)
    
    def has_permission(self, permission_name: str) -> bool:
        """Verificar si el rol tiene un permiso específico"""
        return any(p.name == permission_name for p in self.permissions)
    
    def deactivate(self) -> None:
        """Desactivar rol"""
        self.is_active = False
```

### Permission Entity
```python
# modules/rbac/domain/entity/permission.py
class Permission:
    def __init__(self, name: str, resource: str, action: str, description: str = ""):
        self.name = name
        self.resource = resource
        self.action = action
        self.description = description
        self.is_active = True
        self.created_at = datetime.now()
    
    def __str__(self) -> str:
        return f"{self.resource}:{self.action}"
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Permission):
            return False
        return self.name == other.name
```

## Casos de Uso

### Gestión de Roles
```python
# modules/rbac/domain/usecase/role.py
class CreateRoleUseCase:
    def __init__(self, repository: RoleRepository):
        self.repository = repository
    
    def execute(self, name: str, description: str) -> Role:
        # Verificar que no existe
        if self.repository.find_by_name(name):
            raise RoleAlreadyExistsError(f"Role {name} already exists")
        
        # Crear rol
        role = Role(name, description)
        return self.repository.save(role)

class AssignPermissionToRoleUseCase:
    def __init__(self, role_repository: RoleRepository, 
                 permission_repository: PermissionRepository):
        self.role_repository = role_repository
        self.permission_repository = permission_repository
    
    def execute(self, role_id: int, permission_id: int) -> Role:
        role = self.role_repository.find_by_id(role_id)
        if not role:
            raise RoleNotFoundError()
        
        permission = self.permission_repository.find_by_id(permission_id)
        if not permission:
            raise PermissionNotFoundError()
        
        role.add_permission(permission)
        return self.role_repository.save(role)
```

### Asignación de Roles a Usuarios
```python
# modules/rbac/domain/usecase/user_role.py
class AssignRoleToUserUseCase:
    def __init__(self, repository: RBACRepository):
        self.repository = repository
    
    def execute(self, user_id: int, role_id: int) -> None:
        # Verificar que el usuario existe
        if not self.repository.user_exists(user_id):
            raise UserNotFoundError()
        
        # Verificar que el rol existe
        role = self.repository.find_role_by_id(role_id)
        if not role or not role.is_active:
            raise RoleNotFoundError()
        
        # Asignar rol
        self.repository.assign_role_to_user(user_id, role_id)
```

## Servicios de Aplicación

### RoleService
```python
# modules/rbac/application/service/role.py
class RoleService:
    def __init__(self, repository: RBACRepository):
        self.repository = repository
        self.create_role_usecase = CreateRoleUseCase(repository)
        self.assign_permission_usecase = AssignPermissionToRoleUseCase(repository, repository)
    
    def create_role(self, name: str, description: str) -> RoleDTO:
        """Crear nuevo rol"""
        role = self.create_role_usecase.execute(name, description)
        
        # Publicar evento
        event = DomainEvent(
            event_type="role_created",
            data={"role_id": role.id, "name": name},
            timestamp=datetime.now(),
            module_source="rbac"
        )
        event_bus.publish(event)
        
        return RoleDTO.from_entity(role)
    
    def assign_permission_to_role(self, role_id: int, permission_id: int) -> RoleDTO:
        """Asignar permiso a rol"""
        role = self.assign_permission_usecase.execute(role_id, permission_id)
        return RoleDTO.from_entity(role)
    
    def get_user_roles(self, user_id: int) -> List[RoleDTO]:
        """Obtener roles de un usuario"""
        roles = self.repository.get_user_roles(user_id)
        return [RoleDTO.from_entity(role) for role in roles]
    
    def check_user_permission(self, user_id: int, permission_name: str) -> bool:
        """Verificar si un usuario tiene un permiso específico"""
        user_roles = self.repository.get_user_roles(user_id)
        
        for role in user_roles:
            if role.has_permission(permission_name):
                return True
        
        return False
```

## Roles Predefinidos

### Roles del Sistema
```python
# modules/rbac/domain/entity/system_roles.py
class SystemRoles:
    SUPER_ADMIN = "super_admin"
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"
    
    @classmethod
    def get_default_roles(cls) -> List[Dict[str, str]]:
        return [
            {
                "name": cls.SUPER_ADMIN,
                "description": "Super administrador con acceso total"
            },
            {
                "name": cls.ADMIN,
                "description": "Administrador del sistema"
            },
            {
                "name": cls.USER,
                "description": "Usuario estándar"
            },
            {
                "name": cls.GUEST,
                "description": "Usuario invitado con acceso limitado"
            }
        ]
```

### Inicialización de Roles
```python
# scripts/init_roles.py
def initialize_system_roles():
    """Inicializar roles del sistema"""
    role_service = service_locator.get_service("role_service")
    
    for role_data in SystemRoles.get_default_roles():
        try:
            role_service.create_role(
                name=role_data["name"],
                description=role_data["description"]
            )
            print(f"✅ Role created: {role_data['name']}")
        except RoleAlreadyExistsError:
            print(f"⚠️  Role already exists: {role_data['name']}")
```

## Jerarquía de Roles

### Herencia de Permisos
```python
# modules/rbac/domain/entity/role_hierarchy.py
class RoleHierarchy:
    """Define la jerarquía de roles"""
    
    HIERARCHY = {
        "super_admin": ["admin", "user", "guest"],
        "admin": ["user", "guest"],
        "user": ["guest"],
        "guest": []
    }
    
    @classmethod
    def get_inherited_roles(cls, role_name: str) -> List[str]:
        """Obtener roles heredados"""
        return cls.HIERARCHY.get(role_name, [])
    
    @classmethod
    def has_role_or_higher(cls, user_roles: List[str], required_role: str) -> bool:
        """Verificar si el usuario tiene el rol requerido o uno superior"""
        for user_role in user_roles:
            if user_role == required_role:
                return True
            
            inherited_roles = cls.get_inherited_roles(user_role)
            if required_role in inherited_roles:
                return True
        
        return False
```

## Decoradores de Autorización

### Decorador de Rol Requerido
```python
# modules/rbac/shared/decorators.py
from functools import wraps
from fastapi import HTTPException, Depends
from modules.auth.application.service.jwt import get_current_user

def require_role(required_role: str):
    """Decorador que requiere un rol específico"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Obtener usuario actual
            current_user = kwargs.get('current_user')
            if not current_user:
                raise HTTPException(status_code=401, detail="Authentication required")
            
            # Verificar rol
            rbac_service = service_locator.get_service("rbac_service")
            user_roles = rbac_service.get_user_roles(current_user.id)
            role_names = [role.name for role in user_roles]
            
            if not RoleHierarchy.has_role_or_higher(role_names, required_role):
                raise HTTPException(status_code=403, detail="Insufficient permissions")
            
            return await func(*args, **kwargs)
        return wrapper
    return decorator

# Uso del decorador
@router.get("/admin/users")
@require_role("admin")
async def get_all_users(current_user: User = Depends(get_current_user)):
    # Solo usuarios con rol admin o superior pueden acceder
    pass
```

## API Endpoints

### Gestión de Roles
```python
# modules/rbac/adapter/input/api/v1/rbac.py
@router.post("/roles", response_model=RoleResponse)
async def create_role(
    request: CreateRoleRequest,
    role_service: RoleService = Depends(),
    current_user: User = Depends(get_current_user)
):
    """Crear nuevo rol"""
    # Verificar permisos
    if not has_permission(current_user, "rbac:create_role"):
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    
    role_dto = role_service.create_role(request.name, request.description)
    return RoleResponse.from_dto(role_dto)

@router.post("/users/{user_id}/roles/{role_id}")
async def assign_role_to_user(
    user_id: int,
    role_id: int,
    role_service: RoleService = Depends(),
    current_user: User = Depends(get_current_user)
):
    """Asignar rol a usuario"""
    if not has_permission(current_user, "rbac:assign_role"):
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    
    role_service.assign_role_to_user(user_id, role_id)
    return {"message": "Role assigned successfully"}

@router.get("/users/{user_id}/roles", response_model=List[RoleResponse])
async def get_user_roles(
    user_id: int,
    role_service: RoleService = Depends(),
    current_user: User = Depends(get_current_user)
):
    """Obtener roles de un usuario"""
    if not has_permission(current_user, "rbac:view_roles"):
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    
    roles = role_service.get_user_roles(user_id)
    return [RoleResponse.from_dto(role) for role in roles]
```

## Middleware de Autorización

### Middleware RBAC
```python
# core/fastapi/middlewares/rbac.py
class RBACMiddleware:
    def __init__(self, app):
        self.app = app
    
    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            request = Request(scope, receive)
            
            # Verificar si la ruta requiere autorización
            if self._requires_authorization(request.url.path):
                user = await self._get_current_user(request)
                if not user:
                    response = JSONResponse(
                        status_code=401,
                        content={"detail": "Authentication required"}
                    )
                    await response(scope, receive, send)
                    return
                
                # Verificar permisos
                if not await self._check_permissions(user, request):
                    response = JSONResponse(
                        status_code=403,
                        content={"detail": "Insufficient permissions"}
                    )
                    await response(scope, receive, send)
                    return
        
        await self.app(scope, receive, send)
```

## Testing del Sistema de Roles

### Tests Unitarios
```python
# tests/unit/rbac/test_role_service.py
class TestRoleService:
    def test_create_role_success(self):
        # Arrange
        mock_repository = Mock(spec=RBACRepository)
        mock_repository.find_by_name.return_value = None
        service = RoleService(mock_repository)
        
        # Act
        result = service.create_role("test_role", "Test role")
        
        # Assert
        assert result.name == "test_role"
        mock_repository.save.assert_called_once()
    
    def test_assign_role_to_user_success(self):
        # Arrange
        mock_repository = Mock(spec=RBACRepository)
        mock_repository.user_exists.return_value = True
        mock_repository.find_role_by_id.return_value = Role("test_role", "Test")
        service = RoleService(mock_repository)
        
        # Act
        service.assign_role_to_user(1, 1)
        
        # Assert
        mock_repository.assign_role_to_user.assert_called_once_with(1, 1)
```

### Tests de Integración
```python
# tests/integration/rbac/test_rbac_endpoints.py
class TestRBACEndpoints:
    async def test_create_role_with_admin_user(self, client, admin_user):
        # Arrange
        headers = {"Authorization": f"Bearer {admin_user.token}"}
        data = {"name": "new_role", "description": "New role"}
        
        # Act
        response = await client.post("/rbac/roles", json=data, headers=headers)
        
        # Assert
        assert response.status_code == 201
        assert response.json()["name"] == "new_role"
    
    async def test_create_role_without_permission_fails(self, client, regular_user):
        # Arrange
        headers = {"Authorization": f"Bearer {regular_user.token}"}
        data = {"name": "new_role", "description": "New role"}
        
        # Act
        response = await client.post("/rbac/roles", json=data, headers=headers)
        
        # Assert
        assert response.status_code == 403
```