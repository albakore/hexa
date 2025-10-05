# Buenas Prácticas

## Principios Generales

### 1. Separación de Responsabilidades

Cada capa tiene una responsabilidad específica:

```python
# ✅ Correcto - Responsabilidades separadas
class UserService:  # Lógica de negocio
    async def create_user(self, command: CreateUserCommand) -> User:
        # Validaciones de negocio
        if not command.email:
            raise ValueError("Email is required")
        return await self.repository.save(User(**command.dict()))

class UserController:  # Manejo de HTTP
    async def create_user(self, request: CreateUserRequest):
        command = CreateUserCommand(**request.dict())
        return await self.service.create_user(command)

# ❌ Incorrecto - Responsabilidades mezcladas
class UserService:
    async def create_user(self, request: HTTPRequest):  # ❌ HTTP en servicio
        if request.method != "POST":  # ❌ Lógica HTTP
            raise HTTPException(405)
        # ...
```

### 2. Inversión de Dependencias

Depende de abstracciones, no de implementaciones concretas:

```python
# ✅ Correcto - Depende de interfaz
class UserService:
    def __init__(self, repository: UserRepositoryInterface):
        self.repository = repository

# ❌ Incorrecto - Depende de implementación
class UserService:
    def __init__(self):
        self.repository = SQLUserRepository()  # ❌ Acoplamiento fuerte
```

## Arquitectura de Módulos

### Estructura de Directorios

```
modules/[module_name]/
├── adapter/
│   ├── input/
│   │   └── api/v1/          # Controladores REST
│   └── output/
│       └── persistence/     # Repositorios
├── application/
│   ├── service/            # Servicios de aplicación
│   └── dto/               # DTOs y comandos
├── domain/
│   ├── entity/            # Entidades de dominio
│   ├── repository/        # Interfaces de repositorio
│   └── usecase/          # Casos de uso (opcional)
├── container.py          # Inyección de dependencias
└── module.py            # Definición del módulo
```

### Naming Conventions

```python
# Archivos
user_service.py          # snake_case
CreateUserCommand        # PascalCase para clases
get_user_by_id          # snake_case para funciones

# Clases
class UserService:       # PascalCase
class UserRepository:    # PascalCase
class CreateUserCommand: # PascalCase

# Variables y funciones
user_service = ...       # snake_case
async def create_user(): # snake_case

# Constantes
MAX_USERS = 100         # UPPER_CASE
```

## Dependency Injection

### Configuración de Containers

```python
# ✅ Correcto - Container bien estructurado
class UserContainer(DeclarativeContainer):
    # Dependencias externas primero
    db_session = Object(session)
    
    # Repositorios como Singleton
    repository = Singleton(
        UserSQLAlchemyRepository,
        session=db_session
    )
    
    # Adaptadores como Factory
    repository_adapter = Factory(
        UserRepositoryAdapter,
        repository=repository
    )
    
    # Servicios como Factory
    service = Factory(
        UserService,
        repository=repository_adapter
    )

# ❌ Incorrecto - Todo como Singleton
class UserContainer(DeclarativeContainer):
    service = Singleton(UserService)  # ❌ Servicios stateless no necesitan ser Singleton
```

### Uso de Providers

```python
# ✅ Factory para servicios stateless
service = Factory(UserService, repository=repository)

# ✅ Singleton para recursos compartidos
database = Singleton(DatabaseConnection)

# ✅ Object para instancias existentes
redis_client = Object(redis.Redis())

# ❌ Evitar Singleton para servicios con estado
user_cache = Singleton(UserCache)  # ❌ Si tiene estado mutable
```

## Service Locator

### Registro de Servicios

```python
# ✅ Correcto - Nombres descriptivos y consistentes
@property
def service(self) -> Dict[str, object]:
    return {
        "user_service": self._container.service,
        "user.notification_service": self._container.notification_service,
    }

# ❌ Incorrecto - Nombres inconsistentes
@property
def service(self) -> Dict[str, object]:
    return {
        "users": self._container.service,  # ❌ Inconsistente
        "userNotifications": self._container.notification_service,  # ❌ camelCase
    }
```

### Uso en Servicios

```python
# ✅ Correcto - Validar existencia del servicio
class UserService:
    async def assign_role(self, user_id: str, role_id: int):
        rbac_service = service_locator.get_service("rbac.role_service")
        if not rbac_service:
            raise ServiceUnavailableError("RBAC service not available")
        
        return await rbac_service.assign_role_to_user(user_id, role_id)

# ❌ Incorrecto - No validar servicio
class UserService:
    async def assign_role(self, user_id: str, role_id: int):
        rbac_service = service_locator.get_service("rbac.role_service")
        return await rbac_service.assign_role_to_user(user_id, role_id)  # ❌ Puede fallar
```

## FastAPI Routes

### Inyección de Dependencias

```python
# ✅ Correcto - Patrón híbrido
@user_router.post("")
@inject
async def create_user(
    request: CreateUserRequest,
    # Servicio interno - tipado fuerte
    user_service: UserService = Depends(Provide[UserContainer.service]),
    # Servicios externos - desacoplados
    auth_service = Depends(service_locator.get_dependency("auth_service")),
):
    # Validar autenticación
    current_user = await auth_service.get_current_user()
    if not current_user:
        raise HTTPException(401, "Unauthorized")
    
    return await user_service.create_user(request)

# ❌ Incorrecto - Mezclar patrones sin razón
@user_router.post("")
async def create_user(
    request: CreateUserRequest,
    user_service = Depends(service_locator.get_dependency("user_service")),  # ❌ Interno como externo
):
    pass
```

### Manejo de Errores

```python
# ✅ Correcto - Manejo específico de errores
@user_router.post("")
async def create_user(request: CreateUserRequest, service: UserService = ...):
    try:
        return await service.create_user(request)
    except ValidationError as e:
        raise HTTPException(400, f"Validation error: {e}")
    except DuplicateEmailError as e:
        raise HTTPException(409, "Email already exists")
    except Exception as e:
        logger.error(f"Unexpected error creating user: {e}")
        raise HTTPException(500, "Internal server error")

# ❌ Incorrecto - Manejo genérico
@user_router.post("")
async def create_user(request: CreateUserRequest, service: UserService = ...):
    try:
        return await service.create_user(request)
    except Exception:  # ❌ Muy genérico
        raise HTTPException(500, "Error")
```

## Testing

### Estructura de Tests

```
tests/
├── unit/
│   └── modules/
│       └── user/
│           ├── test_user_service.py
│           └── test_user_repository.py
├── integration/
│   └── modules/
│       └── user/
│           └── test_user_api.py
└── fixtures/
    ├── database.py
    └── services.py
```

### Tests Unitarios

```python
# ✅ Correcto - Mock de dependencias
@pytest.mark.asyncio
async def test_create_user_success():
    # Arrange
    mock_repository = AsyncMock()
    mock_repository.save.return_value = User(id=1, email="test@example.com")
    
    service = UserService(mock_repository)
    command = CreateUserCommand(email="test@example.com")
    
    # Act
    result = await service.create_user(command)
    
    # Assert
    assert result.email == "test@example.com"
    mock_repository.save.assert_called_once()

# ❌ Incorrecto - Dependencias reales en test unitario
async def test_create_user():
    service = UserService(SQLUserRepository())  # ❌ Dependencia real
    result = await service.create_user(command)
```

### Tests de Integración

```python
# ✅ Correcto - Test de integración con DB real
@pytest.mark.asyncio
async def test_user_creation_integration(db_session):
    # Usar base de datos de test real
    repository = UserSQLAlchemyRepository(db_session)
    service = UserService(UserRepositoryAdapter(repository))
    
    command = CreateUserCommand(email="integration@test.com")
    result = await service.create_user(command)
    
    # Verificar en DB
    saved_user = await repository.find_by_email("integration@test.com")
    assert saved_user is not None
```

## Performance

### Lazy Loading

```python
# ✅ Correcto - Lazy loading de servicios pesados
class UserService:
    def __init__(self, repository: UserRepositoryInterface):
        self.repository = repository
        self._analytics_service = None
    
    @property
    def analytics_service(self):
        if self._analytics_service is None:
            self._analytics_service = service_locator.get_service("analytics_service")
        return self._analytics_service

# ❌ Incorrecto - Cargar todo en __init__
class UserService:
    def __init__(self, repository: UserRepositoryInterface):
        self.repository = repository
        self.analytics_service = service_locator.get_service("analytics_service")  # ❌ Siempre carga
```

### Caching

```python
# ✅ Correcto - Cache con TTL
from functools import lru_cache
from datetime import datetime, timedelta

class UserService:
    def __init__(self):
        self._role_cache = {}
        self._cache_ttl = timedelta(minutes=5)
    
    async def get_user_roles(self, user_id: str):
        cache_key = f"user_roles_{user_id}"
        cached_data = self._role_cache.get(cache_key)
        
        if cached_data and datetime.now() - cached_data['timestamp'] < self._cache_ttl:
            return cached_data['data']
        
        roles = await self._fetch_user_roles(user_id)
        self._role_cache[cache_key] = {
            'data': roles,
            'timestamp': datetime.now()
        }
        return roles
```

## Security

### Validación de Input

```python
# ✅ Correcto - Validación exhaustiva
class CreateUserCommand(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    name: str = Field(min_length=1, max_length=100)
    
    @validator('password')
    def validate_password(cls, v):
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain uppercase letter')
        if not re.search(r'[0-9]', v):
            raise ValueError('Password must contain number')
        return v

# ❌ Incorrecto - Validación mínima
class CreateUserCommand(BaseModel):
    email: str  # ❌ No valida formato
    password: str  # ❌ No valida complejidad
```

### Sanitización

```python
# ✅ Correcto - Sanitizar input
import html

class UserService:
    async def create_user(self, command: CreateUserCommand):
        # Sanitizar datos de entrada
        sanitized_name = html.escape(command.name.strip())
        
        user = User(
            email=command.email.lower().strip(),
            name=sanitized_name
        )
        return await self.repository.save(user)
```

## Logging

### Structured Logging

```python
# ✅ Correcto - Logging estructurado
import structlog

logger = structlog.get_logger(__name__)

class UserService:
    async def create_user(self, command: CreateUserCommand):
        logger.info(
            "Creating user",
            email=command.email,
            module="user_service",
            action="create_user"
        )
        
        try:
            user = await self.repository.save(User(**command.dict()))
            logger.info(
                "User created successfully",
                user_id=user.id,
                email=user.email
            )
            return user
        except Exception as e:
            logger.error(
                "Failed to create user",
                email=command.email,
                error=str(e),
                exc_info=True
            )
            raise

# ❌ Incorrecto - Logging básico
import logging

logger = logging.getLogger(__name__)

class UserService:
    async def create_user(self, command: CreateUserCommand):
        logger.info("Creating user")  # ❌ Poca información
        user = await self.repository.save(User(**command.dict()))
        logger.info("User created")  # ❌ No identifica qué usuario
```

## Documentation

### Docstrings

```python
# ✅ Correcto - Docstring completo
class UserService:
    """Service for managing user operations.
    
    This service handles user creation, updates, and role management.
    It coordinates between the user repository and external services.
    """
    
    async def create_user(self, command: CreateUserCommand) -> User:
        """Create a new user in the system.
        
        Args:
            command: Command containing user creation data
            
        Returns:
            User: The created user entity
            
        Raises:
            ValidationError: If user data is invalid
            DuplicateEmailError: If email already exists
            
        Example:
            >>> command = CreateUserCommand(email="user@example.com", name="John")
            >>> user = await service.create_user(command)
            >>> print(user.id)
            1
        """
        # Implementation...

# ❌ Incorrecto - Sin documentación
class UserService:
    async def create_user(self, command):  # ❌ Sin tipos ni docstring
        pass
```

### API Documentation

```python
# ✅ Correcto - Documentación completa de API
@user_router.post(
    "",
    response_model=UserResponse,
    status_code=201,
    summary="Create a new user",
    description="Creates a new user account with the provided information",
    responses={
        201: {"description": "User created successfully"},
        400: {"description": "Invalid user data"},
        409: {"description": "Email already exists"},
    }
)
async def create_user(
    request: CreateUserRequest = Body(..., description="User creation data"),
    service: UserService = Depends(Provide[UserContainer.service])
) -> UserResponse:
    """Create a new user account."""
    return await service.create_user(request)
```