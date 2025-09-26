# Gestión de Permisos

## Definición de Permisos

Los permisos definen acciones específicas que pueden realizarse sobre recursos del sistema. Cada permiso sigue el formato `resource:action`.

## Estructura de Permisos

### Formato Estándar
```
resource:action
```

**Ejemplos**:
- `user:create` - Crear usuarios
- `user:read` - Leer información de usuarios
- `user:update` - Actualizar usuarios
- `user:delete` - Eliminar usuarios
- `rbac:assign_role` - Asignar roles
- `finance:view_reports` - Ver reportes financieros

### Entidad Permission
```python
# modules/rbac/domain/entity/permission.py
class Permission:
    def __init__(self, name: str, resource: str, action: str, description: str = ""):
        self.name = name  # Nombre único del permiso
        self.resource = resource  # Recurso sobre el que actúa
        self.action = action  # Acción específica
        self.description = description
        self.is_active = True
        self.created_at = datetime.now()
    
    @property
    def full_name(self) -> str:
        """Nombre completo del permiso"""
        return f"{self.resource}:{self.action}"
    
    def matches(self, resource: str, action: str) -> bool:
        """Verificar si el permiso coincide con recurso y acción"""
        return self.resource == resource and self.action == action
    
    def __str__(self) -> str:
        return self.full_name
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Permission):
            return False
        return self.name == other.name
```

## Casos de Uso de Permisos

### Crear Permiso
```python
# modules/rbac/domain/usecase/permission.py
class CreatePermissionUseCase:
    def __init__(self, repository: PermissionRepository):
        self.repository = repository
    
    def execute(self, name: str, resource: str, action: str, description: str = "") -> Permission:
        # Verificar que no existe
        if self.repository.find_by_name(name):
            raise PermissionAlreadyExistsError(f"Permission {name} already exists")
        
        # Verificar formato
        if not self._is_valid_format(resource, action):
            raise InvalidPermissionFormatError()
        
        # Crear permiso
        permission = Permission(name, resource, action, description)
        return self.repository.save(permission)
    
    def _is_valid_format(self, resource: str, action: str) -> bool:
        """Validar formato de recurso y acción"""
        return (
            resource and action and
            resource.isalnum() and action.isalnum() and
            len(resource) > 0 and len(action) > 0
        )
```

### Verificar Permiso
```python
# modules/rbac/domain/usecase/permission.py
class CheckPermissionUseCase:
    def __init__(self, rbac_repository: RBACRepository):
        self.repository = rbac_repository
    
    def execute(self, user_id: int, resource: str, action: str) -> bool:
        """Verificar si un usuario tiene permiso para una acción específica"""
        # Obtener roles del usuario
        user_roles = self.repository.get_user_roles(user_id)
        
        # Verificar permisos en cada rol
        for role in user_roles:
            if not role.is_active:
                continue
                
            for permission in role.permissions:
                if permission.matches(resource, action) and permission.is_active:
                    return True
        
        return False
```

## Servicio de Permisos

### PermissionService
```python
# modules/rbac/application/service/permission.py
class PermissionService:
    def __init__(self, repository: RBACRepository):
        self.repository = repository
        self.create_permission_usecase = CreatePermissionUseCase(repository)
        self.check_permission_usecase = CheckPermissionUseCase(repository)
    
    def create_permission(self, name: str, resource: str, action: str, 
                         description: str = "") -> PermissionDTO:
        """Crear nuevo permiso"""
        permission = self.create_permission_usecase.execute(name, resource, action, description)
        
        # Publicar evento
        event = DomainEvent(
            event_type="permission_created",
            data={
                "permission_id": permission.id,
                "name": name,
                "resource": resource,
                "action": action
            },
            timestamp=datetime.now(),
            module_source="rbac"
        )
        event_bus.publish(event)
        
        return PermissionDTO.from_entity(permission)
    
    def check_user_permission(self, user_id: int, resource: str, action: str) -> bool:
        """Verificar si un usuario tiene un permiso específico"""
        return self.check_permission_usecase.execute(user_id, resource, action)
    
    def get_user_permissions(self, user_id: int) -> List[PermissionDTO]:
        """Obtener todos los permisos de un usuario"""
        user_roles = self.repository.get_user_roles(user_id)
        permissions = set()
        
        for role in user_roles:
            if role.is_active:
                for permission in role.permissions:
                    if permission.is_active:
                        permissions.add(permission)
        
        return [PermissionDTO.from_entity(p) for p in permissions]
    
    def get_role_permissions(self, role_id: int) -> List[PermissionDTO]:
        """Obtener permisos de un rol específico"""
        role = self.repository.find_role_by_id(role_id)
        if not role:
            raise RoleNotFoundError()
        
        return [PermissionDTO.from_entity(p) for p in role.permissions if p.is_active]
```

## Permisos Predefinidos

### Permisos del Sistema
```python
# modules/rbac/domain/entity/system_permissions.py
class SystemPermissions:
    """Permisos predefinidos del sistema"""
    
    # Permisos de usuarios
    USER_CREATE = "user:create"
    USER_READ = "user:read"
    USER_UPDATE = "user:update"
    USER_DELETE = "user:delete"
    USER_LIST = "user:list"
    
    # Permisos de RBAC
    RBAC_CREATE_ROLE = "rbac:create_role"
    RBAC_UPDATE_ROLE = "rbac:update_role"
    RBAC_DELETE_ROLE = "rbac:delete_role"
    RBAC_ASSIGN_ROLE = "rbac:assign_role"
    RBAC_CREATE_PERMISSION = "rbac:create_permission"
    RBAC_VIEW_ROLES = "rbac:view_roles"
    RBAC_VIEW_PERMISSIONS = "rbac:view_permissions"
    
    # Permisos de finanzas
    FINANCE_VIEW_REPORTS = "finance:view_reports"
    FINANCE_CREATE_CURRENCY = "finance:create_currency"
    FINANCE_MANAGE_ACCOUNTING = "finance:manage_accounting"
    
    # Permisos de proveedores
    PROVIDER_CREATE = "provider:create"
    PROVIDER_UPDATE = "provider:update"
    PROVIDER_DELETE = "provider:delete"
    PROVIDER_VIEW = "provider:view"
    
    @classmethod
    def get_all_permissions(cls) -> List[Dict[str, str]]:
        """Obtener todos los permisos del sistema"""
        permissions = []
        
        # Usar reflexión para obtener todas las constantes
        for attr_name in dir(cls):
            if not attr_name.startswith('_') and attr_name.isupper():
                permission_name = getattr(cls, attr_name)
                if ':' in permission_name:
                    resource, action = permission_name.split(':', 1)
                    permissions.append({
                        'name': permission_name,
                        'resource': resource,
                        'action': action,
                        'description': cls._get_permission_description(permission_name)
                    })
        
        return permissions
    
    @classmethod
    def _get_permission_description(cls, permission_name: str) -> str:
        """Obtener descripción de un permiso"""
        descriptions = {
            cls.USER_CREATE: "Crear nuevos usuarios",
            cls.USER_READ: "Ver información de usuarios",
            cls.USER_UPDATE: "Actualizar información de usuarios",
            cls.USER_DELETE: "Eliminar usuarios",
            cls.RBAC_CREATE_ROLE: "Crear nuevos roles",
            cls.RBAC_ASSIGN_ROLE: "Asignar roles a usuarios",
            cls.FINANCE_VIEW_REPORTS: "Ver reportes financieros",
            cls.PROVIDER_CREATE: "Crear nuevos proveedores",
            # ... más descripciones
        }
        return descriptions.get(permission_name, "")
```

### Inicialización de Permisos
```python
# scripts/init_permissions.py
def initialize_system_permissions():
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
            print(f"✅ Permission created: {perm_data['name']}")
        except PermissionAlreadyExistsError:
            print(f"⚠️  Permission already exists: {perm_data['name']}")
```

## Decoradores de Permisos

### Decorador de Permiso Requerido
```python
# shared/decorators/permission.py
from functools import wraps
from fastapi import HTTPException, Depends

def require_permission(resource: str, action: str):
    """Decorador que requiere un permiso específico"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Obtener usuario actual
            current_user = kwargs.get('current_user')
            if not current_user:
                raise HTTPException(status_code=401, detail="Authentication required")
            
            # Verificar permiso
            permission_service = service_locator.get_service("permission_service")
            has_permission = permission_service.check_user_permission(
                current_user.id, resource, action
            )
            
            if not has_permission:
                raise HTTPException(
                    status_code=403, 
                    detail=f"Permission required: {resource}:{action}"
                )
            
            return await func(*args, **kwargs)
        return wrapper
    return decorator

# Uso del decorador
@router.post("/users")
@require_permission("user", "create")
async def create_user(
    request: CreateUserRequest,
    current_user: User = Depends(get_current_user)
):
    # Solo usuarios con permiso user:create pueden acceder
    pass
```

### Decorador de Múltiples Permisos
```python
def require_any_permission(*permissions):
    """Decorador que requiere al menos uno de los permisos especificados"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            current_user = kwargs.get('current_user')
            if not current_user:
                raise HTTPException(status_code=401, detail="Authentication required")
            
            permission_service = service_locator.get_service("permission_service")
            
            # Verificar si tiene al menos uno de los permisos
            for resource, action in permissions:
                if permission_service.check_user_permission(current_user.id, resource, action):
                    return await func(*args, **kwargs)
            
            raise HTTPException(
                status_code=403,
                detail=f"One of these permissions required: {permissions}"
            )
        return wrapper
    return decorator

# Uso
@router.get("/admin/dashboard")
@require_any_permission(("admin", "view"), ("super_admin", "view"))
async def admin_dashboard(current_user: User = Depends(get_current_user)):
    pass
```

## Middleware de Permisos

### Permission Middleware
```python
# core/fastapi/middlewares/permission.py
class PermissionMiddleware:
    def __init__(self, app):
        self.app = app
        self.permission_map = self._build_permission_map()
    
    def _build_permission_map(self) -> Dict[str, Dict[str, Tuple[str, str]]]:
        """Construir mapa de permisos por ruta y método"""
        return {
            "/users": {
                "GET": ("user", "list"),
                "POST": ("user", "create")
            },
            "/users/{id}": {
                "GET": ("user", "read"),
                "PUT": ("user", "update"),
                "DELETE": ("user", "delete")
            },
            "/rbac/roles": {
                "GET": ("rbac", "view_roles"),
                "POST": ("rbac", "create_role")
            }
        }
    
    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            request = Request(scope, receive)
            
            # Verificar si la ruta requiere permisos
            permission = self._get_required_permission(request.url.path, request.method)
            if permission:
                user = await self._get_current_user(request)
                if not user:
                    response = JSONResponse(
                        status_code=401,
                        content={"detail": "Authentication required"}
                    )
                    await response(scope, receive, send)
                    return
                
                # Verificar permiso
                if not await self._check_permission(user, permission):
                    response = JSONResponse(
                        status_code=403,
                        content={"detail": f"Permission required: {permission[0]}:{permission[1]}"}
                    )
                    await response(scope, receive, send)
                    return
        
        await self.app(scope, receive, send)
```

## API Endpoints de Permisos

### Gestión de Permisos
```python
# modules/rbac/adapter/input/api/v1/permission.py
@router.post("/permissions", response_model=PermissionResponse)
async def create_permission(
    request: CreatePermissionRequest,
    permission_service: PermissionService = Depends(),
    current_user: User = Depends(get_current_user)
):
    """Crear nuevo permiso"""
    # Verificar permisos
    if not permission_service.check_user_permission(current_user.id, "rbac", "create_permission"):
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    
    permission_dto = permission_service.create_permission(
        request.name, request.resource, request.action, request.description
    )
    return PermissionResponse.from_dto(permission_dto)

@router.get("/users/{user_id}/permissions", response_model=List[PermissionResponse])
async def get_user_permissions(
    user_id: int,
    permission_service: PermissionService = Depends(),
    current_user: User = Depends(get_current_user)
):
    """Obtener permisos de un usuario"""
    # Verificar que puede ver permisos del usuario
    if current_user.id != user_id:
        if not permission_service.check_user_permission(current_user.id, "rbac", "view_permissions"):
            raise HTTPException(status_code=403, detail="Insufficient permissions")
    
    permissions = permission_service.get_user_permissions(user_id)
    return [PermissionResponse.from_dto(perm) for perm in permissions]

@router.post("/permissions/check")
async def check_permission(
    request: CheckPermissionRequest,
    permission_service: PermissionService = Depends(),
    current_user: User = Depends(get_current_user)
):
    """Verificar si un usuario tiene un permiso específico"""
    has_permission = permission_service.check_user_permission(
        request.user_id, request.resource, request.action
    )
    return {"has_permission": has_permission}
```

## Permisos Granulares

### Permisos a Nivel de Recurso
```python
# Ejemplo: Permisos específicos por recurso
class ResourcePermissions:
    def __init__(self, user_id: int, resource_id: int, resource_type: str):
        self.user_id = user_id
        self.resource_id = resource_id
        self.resource_type = resource_type
        self.permissions: List[str] = []
    
    def add_permission(self, action: str) -> None:
        permission = f"{self.resource_type}:{self.resource_id}:{action}"
        if permission not in self.permissions:
            self.permissions.append(permission)
    
    def has_permission(self, action: str) -> bool:
        permission = f"{self.resource_type}:{self.resource_id}:{action}"
        return permission in self.permissions

# Uso
user_resource_perms = ResourcePermissions(user_id=1, resource_id=123, resource_type="document")
user_resource_perms.add_permission("read")
user_resource_perms.add_permission("edit")

# Verificar
can_edit = user_resource_perms.has_permission("edit")  # True
can_delete = user_resource_perms.has_permission("delete")  # False
```

### Permisos Condicionales
```python
# Ejemplo: Permisos basados en condiciones
class ConditionalPermission:
    def __init__(self, base_permission: Permission, condition: Callable):
        self.base_permission = base_permission
        self.condition = condition
    
    def check(self, user: User, context: dict) -> bool:
        """Verificar permiso con condición"""
        if not self.base_permission.is_active:
            return False
        
        return self.condition(user, context)

# Ejemplo de uso
def owner_condition(user: User, context: dict) -> bool:
    """Solo el propietario puede editar"""
    resource_owner_id = context.get("owner_id")
    return user.id == resource_owner_id

edit_own_document = ConditionalPermission(
    base_permission=Permission("document:edit", "document", "edit"),
    condition=owner_condition
)
```

## Testing de Permisos

### Tests Unitarios
```python
# tests/unit/rbac/test_permission_service.py
class TestPermissionService:
    def test_create_permission_success(self):
        # Arrange
        mock_repository = Mock(spec=RBACRepository)
        mock_repository.find_by_name.return_value = None
        service = PermissionService(mock_repository)
        
        # Act
        result = service.create_permission("test:action", "test", "action", "Test permission")
        
        # Assert
        assert result.name == "test:action"
        mock_repository.save.assert_called_once()
    
    def test_check_user_permission_with_valid_permission_returns_true(self):
        # Arrange
        permission = Permission("test:action", "test", "action")
        role = Role("test_role", "Test role")
        role.add_permission(permission)
        
        mock_repository = Mock(spec=RBACRepository)
        mock_repository.get_user_roles.return_value = [role]
        service = PermissionService(mock_repository)
        
        # Act
        result = service.check_user_permission(1, "test", "action")
        
        # Assert
        assert result is True
```