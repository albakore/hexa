# Módulo User

## Descripción

El módulo **User** es responsable de la gestión completa de usuarios en el sistema. Maneja el CRUD de usuarios, asignación de roles, búsquedas avanzadas y relaciones con otros módulos del sistema.

## Funcionalidades

- ✅ **CRUD completo de usuarios** (crear, leer, actualizar, eliminar)
- ✅ **Listado paginado** de usuarios
- ✅ **Búsqueda avanzada** por roles y módulos
- ✅ **Asignación de roles** a usuarios
- ✅ **Integración con RBAC** para permisos
- ✅ **Validación de datos** con Pydantic
- ✅ **Persistencia en PostgreSQL** con SQLAlchemy

## Arquitectura del Módulo

```mermaid
graph TB
    subgraph "User Module"
        subgraph "Input Adapters"
            UserAPI[User API v1]
        end
        
        subgraph "Application Layer"
            UserService[User Service]
        end
        
        subgraph "Domain Layer"
            UserEntity[User Entity]
            UserRepo[User Repository Interface]
            CreateUserCommand[Create User Command]
        end
        
        subgraph "Output Adapters"
            UserRepoAdapter[User Repository Adapter]
            SQLAlchemyRepo[SQLAlchemy User Repository]
        end
    end
    
    subgraph "External Dependencies"
        PostgreSQL[(PostgreSQL)]
        RBACModule[RBAC Module]
        AppModule[App Module]
    end
    
    UserAPI --> UserService
    UserService --> UserEntity
    UserService --> UserRepo
    UserService --> CreateUserCommand
    UserRepo --> UserRepoAdapter
    UserRepoAdapter --> SQLAlchemyRepo
    SQLAlchemyRepo --> PostgreSQL
    
    UserService -.-> RBACModule
    UserService -.-> AppModule
```

## Servicios Expuestos

```python
@property
def service(self) -> Dict[str, object]:
    return {"user_service": self._container.service}
```

### user_service
- **Propósito**: Gestión completa de usuarios
- **Funciones**: CRUD, búsquedas, asignación de roles
- **Dependencias**: RBAC module, App Module (para búsquedas)

## API Endpoints

### Base Path: `/users/v1/users`

| Método | Endpoint | Descripción | Autenticación |
|--------|----------|-------------|---------------|
| GET | `/` | Listar usuarios (paginado) | Sí |
| GET | `/search` | Búsqueda avanzada por roles/módulos | Sí |
| GET | `/{user_id}` | Obtener usuario por ID | Sí |
| POST | `/` | Crear nuevo usuario | Sí |
| PUT | `/{user_uuid}/role` | Asignar rol a usuario | Sí |

### Ejemplos de Uso

#### Listar Usuarios
```python
# Endpoint: GET /users/v1/users
@user_router.get("")
@inject
async def get_user_list(
    user_service: UserService = Depends(Provide[UserContainer.service]),
    limit: int = Query(default=10, ge=1, le=50),
    page: int = Query(default=0),
):
    return await user_service.get_user_list(int(limit), int(page))
```

**Request:**
```bash
GET /users/v1/users?limit=20&page=0
```

**Response:**
```json
{
    "users": [
        {
            "id": "uuid-123",
            "email": "usuario@ejemplo.com",
            "name": "Juan Pérez",
            "active": true,
            "created_at": "2024-01-15T10:30:00Z"
        }
    ],
    "total": 150,
    "page": 0,
    "limit": 20
}
```

#### Búsqueda Avanzada
```python
# Endpoint: GET /users/v1/users/search
@user_router.get("/search")
@inject
async def search_users(
    token_modules: list[str] = Query(),
    role_service = Depends(service_locator.get_dependency("rbac.role_service")),
    app_module_service = Depends(service_locator.get_dependency("app_module_service")),
    user_service: UserService = Depends(Provide[UserContainer.service]),
):
    # Obtener módulos por tokens
    modules = await app_module_service.get_modules_by_token_name(token_modules)
    
    # Obtener roles de esos módulos
    roles = await role_service.get_all_roles_from_modules(
        [module.id for module in modules]
    )
    
    # Buscar usuarios con esos roles
    users = await user_service.get_all_user_with_roles([role.id for role in roles])
    return users
```

**Request:**
```bash
GET /users/v1/users/search?token_modules=user_management&token_modules=finance
```

#### Crear Usuario
```python
# Endpoint: POST /users/v1/users
@user_router.post("")
@inject
async def create_user(
    user_service: UserService = Depends(Provide[UserContainer.service]),
    request: CreateUserRequest,
):
    command = CreateUserCommand.model_validate(request.model_dump())
    return await user_service.create_user(command=command)
```

**Request:**
```json
{
    "email": "nuevo@usuario.com",
    "name": "Nuevo Usuario",
    "password": "contraseña_segura",
    "active": true
}
```

#### Asignar Rol
```python
# Endpoint: PUT /users/{user_uuid}/role
@user_router.put("/{user_uuid}/role")
@inject
async def assign_role(
    user_service: UserService = Depends(Provide[UserContainer.service]),
    user_uuid: uuid.UUID,
    role: RoleRequest,
):
    return await user_service.assign_role_to_user(str(user_uuid), role.id)
```

## Container de Dependencias

```python
class UserContainer(DeclarativeContainer):
    wiring_config = WiringConfiguration(packages=["."], auto_wire=True)
    
    # Repositorio SQLAlchemy como Singleton
    repository = Singleton(UserSQLAlchemyRepository)
    
    # Adaptador del repositorio como Factory
    repository_adapter = Factory(UserRepositoryAdapter, repository=repository)
    
    # Servicio principal como Factory
    service = Factory(UserService, repository=repository_adapter)
```

### Características del Container

- **Singleton Repository**: Una sola instancia del repositorio SQLAlchemy
- **Factory Service**: Nueva instancia del servicio por request
- **Auto-wiring**: Inyección automática en funciones con `@inject`

## Dependencias Externas

### Módulos Utilizados via Service Locator

```python
# En las rutas que requieren servicios externos
role_service = Depends(service_locator.get_dependency("rbac.role_service"))
app_module_service = Depends(service_locator.get_dependency("app_module_service"))
```

- **RBAC Module**: Para gestión de roles y permisos
- **App Module**: Para búsquedas por módulos del sistema

### Infraestructura
- **PostgreSQL**: Base de datos principal para persistencia
- **SQLAlchemy**: ORM para acceso a datos

## Uso en Otros Módulos

### Obtener Servicio de Usuario

```python
# En otro módulo
from shared.interfaces.service_locator import service_locator

# Obtener el servicio de usuario
user_service = service_locator.get_service("user_service")

# Buscar usuario por email
user = await user_service.get_user_by_email("usuario@ejemplo.com")

# Crear nuevo usuario
command = CreateUserCommand(
    email="nuevo@usuario.com",
    name="Nuevo Usuario"
)
new_user = await user_service.create_user(command)
```

### Inyección en FastAPI

```python
# Para servicios externos al módulo user
@router.get("/user-info")
async def get_user_info(
    user_service = Depends(service_locator.get_dependency("user_service")),
):
    users = await user_service.get_user_list(10, 0)
    return {"users": users}
```

## Modelos de Datos

### CreateUserCommand
```python
class CreateUserCommand(BaseModel):
    email: EmailStr
    name: str = Field(min_length=1, max_length=100)
    password: str = Field(min_length=8)
    active: bool = True
```

### RoleRequest
```python
class RoleRequest(BaseModel):
    id: int  # ID del rol a asignar
```

### UserResponse
```python
class UserResponse(BaseModel):
    id: str
    email: str
    name: str
    active: bool
    created_at: datetime
    roles: List[str] = []
```

## Patrones de Búsqueda

### Búsqueda por Roles y Módulos

El endpoint `/search` implementa un patrón complejo de búsqueda:

1. **Input**: Lista de nombres de módulos/tokens
2. **Proceso**:
   - Obtener módulos por nombres de tokens
   - Extraer roles asociados a esos módulos
   - Buscar usuarios que tengan esos roles
3. **Output**: Lista de usuarios filtrados

```python
# Flujo de búsqueda
token_modules = ["user_management", "finance"]
↓
modules = await app_module_service.get_modules_by_token_name(token_modules)
↓
roles = await role_service.get_all_roles_from_modules([module.id for module in modules])
↓
users = await user_service.get_all_user_with_roles([role.id for role in roles])
```

## Testing

### Test de Creación de Usuario

```python
@pytest.mark.asyncio
async def test_create_user():
    # Mock del repositorio
    mock_repository = AsyncMock()
    mock_repository.save.return_value = User(
        id="uuid-123",
        email="test@example.com",
        name="Test User"
    )
    
    # Test del servicio
    service = UserService(mock_repository)
    command = CreateUserCommand(
        email="test@example.com",
        name="Test User",
        password="password123"
    )
    
    result = await service.create_user(command)
    assert result.email == "test@example.com"
```

### Test de API

```python
@pytest.mark.asyncio
async def test_get_users_endpoint():
    response = await client.get("/users/v1/users?limit=5&page=0")
    
    assert response.status_code == 200
    data = response.json()
    assert "users" in data
    assert len(data["users"]) <= 5
```

## Configuración

### Variables de Entorno

```env
# Database
DATABASE_URL=postgresql://user:password@localhost/dbname

# User Module Specific
USER_DEFAULT_ROLE=user
USER_PASSWORD_MIN_LENGTH=8
USER_EMAIL_VERIFICATION=true
```

## Seguridad

### Validaciones Implementadas

- ✅ **Email válido** con EmailStr de Pydantic
- ✅ **Contraseña mínima** de 8 caracteres
- ✅ **Sanitización de inputs** 
- ✅ **Validación de roles** antes de asignación

### Permisos Requeridos

- **Crear usuario**: Rol admin o manager
- **Listar usuarios**: Usuario autenticado
- **Asignar roles**: Rol admin
- **Actualizar usuario**: Propietario o admin

## Troubleshooting

### Problemas Comunes

1. **Usuario no encontrado**
   - Verificar UUID correcto
   - Revisar si el usuario fue eliminado

2. **Error al asignar rol**
   - Verificar que el rol existe en RBAC
   - Confirmar permisos del usuario actual

3. **Búsqueda sin resultados**
   - Verificar que los módulos existen
   - Confirmar que hay usuarios con esos roles

### Logs Útiles

```python
# Habilitar logs del módulo user
import logging
logging.getLogger('modules.user').setLevel(logging.DEBUG)
```

## Roadmap

### Funcionalidades Futuras

- [ ] **Perfil de usuario** extendido
- [ ] **Avatar/foto** de usuario
- [ ] **Preferencias** de usuario
- [ ] **Historial de actividad**
- [ ] **Grupos de usuarios**
- [ ] **Importación masiva** de usuarios
- [ ] **API de búsqueda** más avanzada
- [ ] **Notificaciones** de usuario