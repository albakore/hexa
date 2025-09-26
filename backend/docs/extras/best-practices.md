# Mejores Prácticas

## Principios Generales

### 1. Arquitectura Hexagonal
- **Separación de responsabilidades**: Cada capa tiene un propósito específico
- **Inversión de dependencias**: El dominio no depende de detalles de implementación
- **Testabilidad**: Cada capa puede ser probada independientemente
- **Flexibilidad**: Fácil intercambio de adaptadores

### 2. Domain-Driven Design (DDD)
- **Ubiquitous Language**: Usar el lenguaje del dominio en el código
- **Bounded Contexts**: Definir límites claros entre dominios
- **Agregados**: Mantener consistencia dentro de límites transaccionales
- **Value Objects**: Usar objetos inmutables para conceptos sin identidad

## Desarrollo de Módulos

### Estructura de Módulos
```python
# ✅ Buena práctica: Estructura clara y consistente
modules/mi_modulo/
├── domain/          # Lógica de negocio pura
├── application/     # Orquestación y casos de uso
├── adapter/         # Interfaces con el exterior
├── container.py     # Inyección de dependencias
└── module.py        # Definición del módulo
```

### Naming Conventions
```python
# ✅ Buena práctica: Nombres descriptivos y consistentes
class UserService:                    # PascalCase para clases
    def create_user(self, email: str): # snake_case para métodos
        pass

USER_CREATED_EVENT = "user_created"   # UPPER_CASE para constantes
user_repository: UserRepository       # snake_case para variables
```

### Manejo de Errores
```python
# ✅ Buena práctica: Excepciones específicas por capa
# Domain exceptions
class UserNotFoundError(DomainError):
    pass

# Application exceptions  
class UserValidationError(ApplicationError):
    pass

# Infrastructure exceptions
class DatabaseConnectionError(InfrastructureError):
    pass

# ❌ Mala práctica: Usar Exception genérica
def get_user(user_id: int):
    if not user_id:
        raise Exception("Invalid user ID")  # Muy genérica
```

### Logging
```python
# ✅ Buena práctica: Logging estructurado y contextual
import logging

logger = logging.getLogger(__name__)

class UserService:
    def create_user(self, email: str) -> User:
        logger.info(f"Creating user with email: {email}")
        
        try:
            user = self.user_repository.save(User(email))
            logger.info(f"User created successfully: {user.id}")
            return user
        except Exception as e:
            logger.error(f"Failed to create user {email}: {e}")
            raise

# ❌ Mala práctica: Print statements
def create_user(self, email: str):
    print(f"Creating user: {email}")  # No usar print
```

## Gestión de Dependencias

### Inyección de Dependencias
```python
# ✅ Buena práctica: Usar dependency injection
class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

# Container configuration
class UserContainer(DeclarativeContainer):
    repository = Singleton(UserSQLAlchemyRepository)
    service = Factory(UserService, repository=repository)

# ❌ Mala práctica: Dependencias hardcodeadas
class UserService:
    def __init__(self):
        self.repository = UserSQLAlchemyRepository()  # Acoplamiento fuerte
```

### Service Locator
```python
# ✅ Buena práctica: Uso responsable del service locator
class AuthService:
    def __init__(self):
        self._user_service = None
    
    @property
    def user_service(self):
        if self._user_service is None:
            self._user_service = service_locator.get_service("user_service")
        return self._user_service

# ❌ Mala práctica: Abuso del service locator
class AuthService:
    def authenticate(self, email: str):
        # Obtener servicios en cada método
        user_service = service_locator.get_service("user_service")
        rbac_service = service_locator.get_service("rbac_service")
        # ...
```

## Comunicación Entre Módulos

### Event-Driven Communication
```python
# ✅ Buena práctica: Eventos bien estructurados
@dataclass
class UserCreatedEvent(DomainEvent):
    user_id: int
    email: str
    created_at: datetime
    
    @property
    def event_type(self) -> str:
        return "user_created"

# Publisher
async def create_user(self, email: str) -> User:
    user = self.repository.save(User(email))
    
    event = UserCreatedEvent(
        user_id=user.id,
        email=user.email,
        created_at=user.created_at
    )
    await event_bus.publish(event)
    
    return user

# ❌ Mala práctica: Eventos genéricos sin estructura
event = DomainEvent(
    event_type="something_happened",
    data={"stuff": "random_data"},  # Datos no estructurados
    timestamp=datetime.now(),
    module_source="unknown"
)
```

### Interfaces Compartidas
```python
# ✅ Buena práctica: Interfaces bien definidas
from abc import ABC, abstractmethod

class UserServiceInterface(ABC):
    @abstractmethod
    async def get_user_by_id(self, user_id: int) -> Optional[UserInfo]:
        pass
    
    @abstractmethod
    async def is_user_active(self, user_id: int) -> bool:
        pass

# ❌ Mala práctica: Dependencias directas entre módulos
from modules.user.application.service.user import UserService  # Acoplamiento directo
```

## Base de Datos

### Modelos y Entidades
```python
# ✅ Buena práctica: Separación clara entre modelos y entidades
# Domain Entity
class User:
    def __init__(self, email: str):
        self.email = self._validate_email(email)
        self.is_active = True
    
    def _validate_email(self, email: str) -> str:
        # Lógica de validación de dominio
        if "@" not in email:
            raise InvalidEmailError()
        return email

# Database Model
class UserModel(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    email = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    
    @classmethod
    def from_entity(cls, user: User) -> 'UserModel':
        return cls(email=user.email, is_active=user.is_active)
    
    def to_entity(self) -> User:
        user = User(self.email)
        user.id = self.id
        user.is_active = self.is_active
        return user
```

### Migraciones
```python
# ✅ Buena práctica: Migraciones descriptivas y reversibles
"""Add user email index

Revision ID: 001_add_user_email_index
Revises: 000_initial
Create Date: 2024-01-01 00:00:00.000000
"""

def upgrade():
    op.create_index('ix_users_email', 'users', ['email'])

def downgrade():
    op.drop_index('ix_users_email', 'users')

# ❌ Mala práctica: Migraciones sin rollback
def upgrade():
    op.add_column('users', sa.Column('new_field', sa.String(50)))

def downgrade():
    pass  # No implementado
```

### Transacciones
```python
# ✅ Buena práctica: Manejo explícito de transacciones
@transactional
async def create_user_with_role(self, email: str, role_id: int) -> User:
    # Toda la operación en una transacción
    user = await self.user_repository.save(User(email))
    await self.rbac_repository.assign_role(user.id, role_id)
    return user

# ❌ Mala práctica: Transacciones implícitas sin control
def create_user_with_role(self, email: str, role_id: int):
    user = self.user_repository.save(User(email))  # Commit automático
    # Si falla aquí, el usuario ya fue creado
    self.rbac_repository.assign_role(user.id, role_id)
```

## APIs y Endpoints

### Request/Response Models
```python
# ✅ Buena práctica: Validación explícita con Pydantic
class CreateUserRequest(BaseModel):
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., min_length=8, description="User password")
    
    @validator('password')
    def validate_password(cls, v):
        if not re.match(r'^(?=.*[A-Za-z])(?=.*\d)', v):
            raise ValueError('Password must contain letters and numbers')
        return v

class UserResponse(BaseModel):
    id: int
    email: str
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# ❌ Mala práctica: Usar diccionarios sin validación
@router.post("/users")
async def create_user(data: dict):  # Sin validación
    email = data.get("email")  # Puede ser None
    password = data.get("password")  # Sin validación
    # ...
```

### Error Handling
```python
# ✅ Buena práctica: Manejo consistente de errores
@router.post("/users", response_model=UserResponse)
async def create_user(request: CreateUserRequest):
    try:
        user = await user_service.create_user(request.email, request.password)
        return UserResponse.from_entity(user)
    except UserAlreadyExistsError as e:
        raise HTTPException(status_code=409, detail=str(e))
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error creating user: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# ❌ Mala práctica: Dejar que las excepciones se propaguen
@router.post("/users")
async def create_user(request: CreateUserRequest):
    user = await user_service.create_user(request.email, request.password)
    return user  # Excepciones no manejadas
```

### Documentación de API
```python
# ✅ Buena práctica: Documentación completa
@router.post(
    "/users",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user",
    description="Create a new user account with email and password",
    responses={
        201: {"description": "User created successfully"},
        409: {"description": "User already exists"},
        422: {"description": "Validation error"}
    }
)
async def create_user(
    request: CreateUserRequest = Body(..., example={
        "email": "user@example.com",
        "password": "securepassword123"
    })
):
    """
    Create a new user account.
    
    - **email**: Valid email address
    - **password**: Minimum 8 characters with letters and numbers
    """
    pass
```

## Testing

### Tests Unitarios
```python
# ✅ Buena práctica: Tests aislados con mocks
class TestUserService:
    def test_create_user_success(self):
        # Arrange
        mock_repository = Mock(spec=UserRepository)
        mock_repository.exists_by_email.return_value = False
        mock_repository.save.return_value = User("test@example.com")
        
        service = UserService(mock_repository)
        
        # Act
        result = service.create_user("test@example.com", "password123")
        
        # Assert
        assert result.email == "test@example.com"
        mock_repository.save.assert_called_once()
    
    def test_create_user_already_exists(self):
        # Arrange
        mock_repository = Mock(spec=UserRepository)
        mock_repository.exists_by_email.return_value = True
        
        service = UserService(mock_repository)
        
        # Act & Assert
        with pytest.raises(UserAlreadyExistsError):
            service.create_user("test@example.com", "password123")

# ❌ Mala práctica: Tests que dependen de base de datos real
class TestUserService:
    def test_create_user(self):
        service = UserService()  # Usa DB real
        user = service.create_user("test@example.com", "password123")
        assert user.email == "test@example.com"
        # No limpia la DB después del test
```

### Tests de Integración
```python
# ✅ Buena práctica: Tests de integración con setup/teardown
class TestUserEndpoints:
    @pytest.fixture(autouse=True)
    def setup(self, test_db):
        self.client = TestClient(app)
        self.test_user = create_test_user()
        yield
        cleanup_test_data()
    
    def test_create_user_endpoint(self):
        response = self.client.post("/users", json={
            "email": "test@example.com",
            "password": "password123"
        })
        
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "test@example.com"
        assert "id" in data
```

## Seguridad

### Autenticación y Autorización
```python
# ✅ Buena práctica: Validación de permisos granular
@router.post("/users")
@require_permission("user", "create")
async def create_user(
    request: CreateUserRequest,
    current_user: User = Depends(get_current_user)
):
    # Solo usuarios con permiso user:create pueden acceder
    pass

# ✅ Buena práctica: Validación de ownership
@router.get("/users/{user_id}")
async def get_user(
    user_id: int,
    current_user: User = Depends(get_current_user)
):
    # Verificar que el usuario puede ver este recurso
    if user_id != current_user.id and not has_permission(current_user, "user", "read_all"):
        raise HTTPException(status_code=403, detail="Access denied")
    
    return await user_service.get_user(user_id)
```

### Validación de Datos
```python
# ✅ Buena práctica: Sanitización y validación
class CreateUserRequest(BaseModel):
    email: EmailStr = Field(..., max_length=255)
    password: SecretStr = Field(..., min_length=8, max_length=128)
    
    @validator('email')
    def sanitize_email(cls, v):
        return v.lower().strip()
    
    @validator('password')
    def validate_password_strength(cls, v):
        password = v.get_secret_value()
        if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])', password):
            raise ValueError('Password must contain uppercase, lowercase, digit and special character')
        return v

# ❌ Mala práctica: Sin validación
class CreateUserRequest(BaseModel):
    email: str  # Sin validación de formato
    password: str  # Sin validación de fortaleza
```

## Performance

### Caching
```python
# ✅ Buena práctica: Cache estratégico
from functools import lru_cache
from cachetools import TTLCache

class UserService:
    def __init__(self):
        self._cache = TTLCache(maxsize=1000, ttl=300)  # 5 minutos
    
    async def get_user_permissions(self, user_id: int) -> List[str]:
        cache_key = f"user_permissions:{user_id}"
        
        if cache_key in self._cache:
            return self._cache[cache_key]
        
        permissions = await self._fetch_user_permissions(user_id)
        self._cache[cache_key] = permissions
        return permissions

# ❌ Mala práctica: Sin cache para operaciones costosas
async def get_user_permissions(self, user_id: int) -> List[str]:
    # Consulta compleja que se ejecuta cada vez
    return await self.repository.get_user_permissions_with_roles(user_id)
```

### Paginación
```python
# ✅ Buena práctica: Paginación eficiente
@router.get("/users", response_model=PaginatedResponse[UserResponse])
async def list_users(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    search: Optional[str] = None
):
    users, total = await user_service.list_users(
        page=page, 
        size=size, 
        search=search
    )
    
    return PaginatedResponse(
        items=[UserResponse.from_entity(u) for u in users],
        total=total,
        page=page,
        size=size,
        pages=math.ceil(total / size)
    )

# ❌ Mala práctica: Retornar todos los registros
@router.get("/users")
async def list_users():
    users = await user_service.get_all_users()  # Puede ser millones
    return users
```

### Queries Optimizadas
```python
# ✅ Buena práctica: Eager loading cuando es necesario
def get_users_with_roles(self) -> List[User]:
    return self.session.query(UserModel)\
        .options(joinedload(UserModel.roles))\
        .all()

# ✅ Buena práctica: Índices apropiados
class UserModel(Base):
    __tablename__ = 'users'
    
    email = Column(String(255), nullable=False, index=True)  # Índice para búsquedas
    created_at = Column(DateTime, default=datetime.now, index=True)  # Para ordenamiento

# ❌ Mala práctica: N+1 queries
def get_users_with_roles(self) -> List[User]:
    users = self.session.query(UserModel).all()
    for user in users:
        user.roles  # Lazy loading - query por cada usuario
    return users
```

## Monitoreo y Observabilidad

### Métricas
```python
# ✅ Buena práctica: Métricas de negocio
from prometheus_client import Counter, Histogram, Gauge

user_creation_counter = Counter('users_created_total', 'Total users created')
request_duration = Histogram('request_duration_seconds', 'Request duration')
active_users_gauge = Gauge('active_users', 'Number of active users')

class UserService:
    async def create_user(self, email: str) -> User:
        with request_duration.time():
            user = await self._create_user_logic(email)
            user_creation_counter.inc()
            return user
```

### Health Checks
```python
# ✅ Buena práctica: Health checks específicos
@router.get("/health/detailed")
async def detailed_health():
    checks = {}
    
    # Database check
    try:
        await database.execute("SELECT 1")
        checks["database"] = "healthy"
    except Exception as e:
        checks["database"] = f"unhealthy: {e}"
    
    # Redis check
    try:
        await redis.ping()
        checks["redis"] = "healthy"
    except Exception as e:
        checks["redis"] = f"unhealthy: {e}"
    
    # External API check
    try:
        response = await external_api.health_check()
        checks["external_api"] = "healthy" if response.ok else "degraded"
    except Exception as e:
        checks["external_api"] = f"unhealthy: {e}"
    
    overall_status = "healthy" if all(
        status == "healthy" for status in checks.values()
    ) else "degraded"
    
    return {
        "status": overall_status,
        "checks": checks,
        "timestamp": datetime.now().isoformat()
    }
```

## Deployment

### Configuración por Entornos
```python
# ✅ Buena práctica: Configuración específica por entorno
class Settings(BaseSettings):
    environment: str = "development"
    debug: bool = False
    database_url: str
    redis_url: str
    
    # Configuración específica por entorno
    @validator('debug')
    def set_debug(cls, v, values):
        if values.get('environment') == 'development':
            return True
        return v
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# ❌ Mala práctica: Hardcodear configuración
DATABASE_URL = "postgresql://user:pass@localhost/db"  # Hardcodeado
DEBUG = True  # Siempre en True
```

### Docker
```dockerfile
# ✅ Buena práctica: Multi-stage build
FROM python:3.11-slim as builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.11-slim as runtime

WORKDIR /app
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY . .

# Usuario no-root
RUN useradd --create-home --shell /bin/bash app
USER app

EXPOSE 8000
CMD ["python", "main.py"]
```

Estas mejores prácticas aseguran que el código sea mantenible, escalable, seguro y eficiente, siguiendo los principios de la arquitectura hexagonal desacoplada.