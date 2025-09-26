# Estructura de Módulos

## Anatomía de un Módulo

Cada módulo sigue una estructura hexagonal estándar que garantiza la separación de responsabilidades y el desacoplamiento. El sistema actual utiliza Service Locator para la comunicación entre módulos y auto-registro para la configuración.

## Estructura de Directorios (Actual)

```
modules/module_name/
├── adapter/
│   ├── input/
│   │   └── api/
│   │       └── v1/
│   │           ├── request/
│   │           │   └── __init__.py
│   │           ├── response/
│   │           │   └── __init__.py
│   │           ├── module_name.py      # Router principal
│   │           └── __init__.py
│   └── output/
│       └── persistence/
│           ├── sqlalchemy/
│           └── repository_adapter.py
├── application/
│   ├── dto/
│   ├── service/
│   └── exception/
├── domain/
│   ├── entity/
│   ├── repository/
│   ├── usecase/
│   ├── vo/
│   └── exception/
├── shared/
│   └── # Utilidades compartidas del módulo
├── test/
│   └── # Tests del módulo
├── __init__.py
├── container.py                       # Dependency Injection
├── module.py                          # Definición del módulo
├── permissions.py                     # Permisos del módulo (opcional)
└── setup.py                          # Configuración del módulo (opcional)
```

## Descripción de Capas

### 1. Domain (Núcleo)
**Ubicación**: `domain/`

**Responsabilidades**:
- Lógica de negocio pura
- Entidades y value objects
- Reglas de dominio
- Casos de uso

**Componentes**:
```python
# domain/entity/user.py
class User:
    def __init__(self, email: str, password: str):
        self.email = self._validate_email(email)
        self.password_hash = self._hash_password(password)
        self.created_at = datetime.now()
    
    def change_password(self, new_password: str) -> None:
        self.password_hash = self._hash_password(new_password)

# domain/repository/user.py
class UserRepository(ABC):
    @abstractmethod
    def save(self, user: User) -> User:
        pass
    
    @abstractmethod
    def find_by_email(self, email: str) -> Optional[User]:
        pass

# domain/usecase/user.py
class CreateUserUseCase:
    def __init__(self, repository: UserRepository):
        self.repository = repository
    
    def execute(self, email: str, password: str) -> User:
        if self.repository.find_by_email(email):
            raise UserAlreadyExistsError()
        
        user = User(email, password)
        return self.repository.save(user)
```

### 2. Application (Orquestación)
**Ubicación**: `application/`

**Responsabilidades**:
- Coordinación de casos de uso
- Transformación de datos
- Validaciones de aplicación
- Manejo de transacciones

**Componentes**:
```python
# application/service/user.py
class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository
        self.create_user_usecase = CreateUserUseCase(repository)
    
    def create_user(self, email: str, password: str) -> UserDTO:
        user = self.create_user_usecase.execute(email, password)
        return UserDTO.from_entity(user)

# application/dto/user.py
@dataclass
class UserDTO:
    id: int
    email: str
    created_at: datetime
    
    @classmethod
    def from_entity(cls, user: User) -> 'UserDTO':
        return cls(
            id=user.id,
            email=user.email,
            created_at=user.created_at
        )
```

### 3. Adapters (Interfaces)
**Ubicación**: `adapter/`

**Responsabilidades**:
- Comunicación con el exterior
- Implementación de interfaces
- Transformación de datos externos
- Integración con servicios

**Input Adapters (Implementación Actual)**:
```python
# adapter/input/api/v1/user.py
from fastapi import APIRouter, Query
from shared.interfaces.service_locator import service_locator

user_router = APIRouter()

def get_user_service():
    return service_locator.get_service("user_service")

@user_router.get("")
async def get_user_list(
    limit: int = Query(default=10, ge=1, le=50),
    page: int = Query(default=0),
):
    user_service = get_user_service()
    if not user_service:
        return {"error": "User service not available"}
    return await user_service.get_user_list(int(limit), int(page))

@user_router.post("")
async def create_user(
    request: dict,  # Simplified for now
):
    user_service = get_user_service()
    if not user_service:
        return {"error": "User service not available"}
    return await user_service.create_user(request)
```

**Output Adapters**:
```python
# adapter/output/persistence/sqlalchemy/user.py
class UserSQLAlchemyRepository(UserRepository):
    def __init__(self, session: Session):
        self.session = session
    
    def save(self, user: User) -> User:
        user_model = UserModel.from_entity(user)
        self.session.add(user_model)
        self.session.commit()
        return user_model.to_entity()
    
    def find_by_email(self, email: str) -> Optional[User]:
        user_model = self.session.query(UserModel).filter_by(email=email).first()
        return user_model.to_entity() if user_model else None
```

## Configuración del Módulo

### Container (Inyección de Dependencias)
```python
# container.py
from dependency_injector import containers, providers
from dependency_injector.wiring import Provide

class UserContainer(containers.DeclarativeContainer):
    """Container de dependencias del módulo User"""
    
    wiring_config = containers.WiringConfiguration(
        modules=[
            "modules.user.adapter.input.api.v1.user",
            "modules.user.application.service.user",
        ]
    )
    
    # Database
    database = providers.Dependency()
    
    # Repositories
    user_repository = providers.Factory(
        "modules.user.adapter.output.persistence.sqlalchemy.user_repository.UserSQLAlchemyRepository",
        session_factory=database.provided.session_factory,
    )
    
    # Services
    user_service = providers.Factory(
        "modules.user.application.service.user.UserService",
        user_repository=user_repository,
    )
```

### Module (Definición del Módulo)
```python
# module.py
from fastapi import APIRouter
from dependency_injector.containers import DeclarativeContainer

from shared.interfaces.module_registry import ModuleInterface
from modules.user.container import UserContainer
from core.fastapi.server.route_helpers import get_routes, set_routes_to_app

class UserModule(ModuleInterface):
    """Módulo de usuarios desacoplado"""
    
    def __init__(self):
        self._container = UserContainer()
        self._routes = self._setup_routes()
    
    @property
    def name(self) -> str:
        return "user"
    
    @property
    def container(self) -> DeclarativeContainer:
        return self._container
    
    @property
    def routes(self) -> APIRouter:
        return self._routes
    
    def _setup_routes(self) -> APIRouter:
        """Configurar las rutas del módulo"""
        from modules.user.adapter.input.api.v1.user import user_router
        return user_router
```

### Setup (Configuración del Módulo)
```python
# setup.py
from core.config.modules import ModuleSetup

class UserModuleSetup(ModuleSetup):
    name = "Users"
    token = "user"
    description = "Gestión de usuarios del sistema"
```

### Permissions (Permisos del Módulo)
```python
# permissions.py
from core.fastapi.dependencies.permission import PermissionGroup

class ModuleUserPermission(PermissionGroup):
    group = "users"
    
    read = "Lee usuarios"
    write = "Crea usuarios"
    update = "Modifica usuarios"
    delete = "Elimina usuarios"
    assign_role = "Asigna roles a usuarios"
```

## Flujo de Datos (Implementación Actual)

```
HTTP Request
    ↓
FastAPI Router (user_router)
    ↓
Depends(get_user_service)
    ↓
@inject + Provide["container.service"]
    ↓
Application Service
    ↓
Domain UseCase
    ↓
Domain Entity
    ↓
Repository Interface
    ↓
Output Adapter (Repository)
    ↓
Database
```

### Comunicación Entre Módulos
```
Módulo A (Controller)
    ↓
Depends(get_service_b)
    ↓
Dependency Injection
    ↓
Módulo B (Service)
    ↓
Event Bus (opcional)
    ↓
Módulo C (Event Handler)
```

## Sistema de Auto-registro

### Registro Automático
```python
# modules/__init__.py
def register_all_modules():
    """Registra todos los módulos disponibles"""
    try:
        # Intentar registro completo
        from modules.user.module import UserModule
        module_registry.register(UserModule())
    except Exception:
        # Fallback: registro simple
        from modules.user.adapter.input.api.v1.user import user_router
        simple_module = SimpleModule("user", user_router)
        module_registry.register(simple_module)
```

### Configuración en el Servidor
```python
# core/fastapi/server/__init__.py
def init_routes_pack(app_: FastAPI):
    """Incluir rutas con prefijos automáticos"""
    modules = module_registry.get_all_modules()
    for name, module in modules.items():
        prefix_map = {
            "user": "/api/v1/users",
            "finance": "/api/v1/finance/currencies",
            "auth": "/api/v1/auth"
        }
        prefix = prefix_map.get(name, f"/api/v1/{name}")
        app_.include_router(module.routes, prefix=prefix, tags=[name.title()])
```

## Reglas de Dependencia

### ✅ Dependencias Permitidas
- **Adapters** → Application
- **Adapters** → Domain
- **Application** → Domain
- **Domain** → Nada (independiente)
- **Cualquier capa** → Service Locator
- **Cualquier capa** → Shared Interfaces

### ❌ Dependencias Prohibidas
- **Domain** → Application
- **Domain** → Adapters
- **Application** → Adapters
- **Módulo** → Otro Módulo (directamente)

### ✅ Comunicación Permitida Entre Módulos
- **Dependency Injection** vía @inject y Provide
- **Event Bus** para comunicación asíncrona
- **Shared Dependencies** para servicios compartidos

## Beneficios de la Estructura Actual

### 1. **Desacoplamiento Total**
- Módulos completamente independientes
- Comunicación vía Service Locator
- Auto-registro automático

### 2. **Simplicidad de Desarrollo**
- Estructura clara y consistente
- Patrones establecidos
- Fácil adición de nuevos módulos

### 3. **Flexibilidad de Despliegue**
- Módulos pueden habilitarse/deshabilitarse
- Configuración externa
- Escalado independiente

### 4. **Mantenibilidad**
- Testing independiente por módulo
- Desarrollo paralelo
- Migración gradual de funcionalidades

### 5. **Sistema de Permisos Integrado**
- Permisos por módulo
- Auto-registro de permisos
- Control granular de acceso

## Convenciones de Nomenclatura

### Archivos
- **Routers**: `user.py`, `currency.py`
- **Repositorios**: `user_repository.py`
- **Servicios**: `user_service.py`
- **DTOs**: `user_dto.py`
- **Módulos**: `module.py`
- **Contenedores**: `container.py`
- **Permisos**: `permissions.py`
- **Setup**: `setup.py`

### Clases
- **Entidades**: `User`, `Currency`
- **Repositorios**: `UserRepository`, `UserSQLAlchemyRepository`
- **Servicios**: `UserService`
- **DTOs**: `UserDTO`, `CreateUserDTO`
- **Módulos**: `UserModule`, `FinanceModule`
- **Permisos**: `ModuleUserPermission`
- **Setup**: `UserModuleSetup`

### Variables de Router
- **Routers**: `user_router`, `currency_router`, `auth_router`
- **Funciones de Servicio**: `get_user_service()`, `get_currency_service()`

### Métodos
- **Repositorios**: `save()`, `find_by_id()`, `find_by_email()`
- **Servicios**: `create_user()`, `update_user()`, `delete_user()`
- **Service Locator**: `get_service()`, `register_service()`
- **Casos de Uso**: `execute()`