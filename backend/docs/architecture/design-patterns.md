# Patrones de Diseño Implementados

## Patrones Arquitectónicos

### 1. Hexagonal Architecture (Ports & Adapters)
**Propósito**: Aislar la lógica de negocio de dependencias externas

```python
# Puerto (Interface)
class UserRepository(ABC):
    @abstractmethod
    def save(self, user: User) -> User:
        pass

# Adaptador (Implementación)
class SQLAlchemyUserRepository(UserRepository):
    def save(self, user: User) -> User:
        # Implementación específica
        pass
```

### 2. Domain-Driven Design (DDD)
**Propósito**: Modelar el software basado en el dominio del negocio

```python
# Entidad de Dominio
class User:
    def __init__(self, email: str, password: str):
        self._validate_email(email)
        self.email = email
        self.password_hash = self._hash_password(password)
    
    def change_password(self, new_password: str) -> None:
        self.password_hash = self._hash_password(new_password)
        # Publicar evento de dominio
        self._events.append(PasswordChangedEvent(self.id))
```

## Patrones de Comunicación

### 1. Service Locator
**Propósito**: Localizar servicios sin dependencias directas

```python
class AuthService:
    def __init__(self):
        self.user_service = service_locator.get_service("user_service")
        self.rbac_service = service_locator.get_service("rbac_service")
    
    def authenticate(self, email: str, password: str) -> Optional[User]:
        user = self.user_service.get_by_email(email)
        if user and self._verify_password(password, user.password_hash):
            return user
        return None
```

### 2. Observer Pattern (Event Bus)
**Propósito**: Comunicación asíncrona entre módulos

```python
# Publisher
class UserService:
    def create_user(self, email: str) -> User:
        user = User(email)
        self.repository.save(user)
        
        # Publicar evento
        event = DomainEvent(
            event_type="user_created",
            data={"user_id": user.id, "email": email},
            timestamp=datetime.now(),
            module_source="user"
        )
        event_bus.publish(event)
        return user

# Subscriber
class EmailNotificationHandler(EventHandler):
    def handle(self, event: DomainEvent) -> None:
        if event.event_type == "user_created":
            self.send_welcome_email(event.data["email"])
```

### 3. Registry Pattern
**Propósito**: Registro centralizado de módulos

```python
class ModuleRegistry:
    def __init__(self):
        self._modules: Dict[str, ModuleInterface] = {}
    
    def register(self, module: ModuleInterface) -> None:
        self._modules[module.name] = module
    
    def get_module(self, name: str) -> Optional[ModuleInterface]:
        return self._modules.get(name)
```

## Patrones de Creación

### 1. Dependency Injection
**Propósito**: Inversión de control para dependencias

```python
class UserContainer(DeclarativeContainer):
    repository = Singleton(UserSQLAlchemyRepository)
    
    service = Factory(
        UserService,
        repository=repository
    )
```

### 2. Factory Pattern
**Propósito**: Creación de objetos complejos

```python
class ModuleFactory:
    @staticmethod
    def create_module(module_type: str) -> ModuleInterface:
        if module_type == "user":
            return UserModule()
        elif module_type == "auth":
            return AuthModule()
        else:
            raise ValueError(f"Unknown module type: {module_type}")
```

## Patrones de Comportamiento

### 1. Strategy Pattern
**Propósito**: Intercambio de algoritmos dinámicamente

```python
class AuthenticationStrategy(ABC):
    @abstractmethod
    def authenticate(self, credentials: dict) -> Optional[User]:
        pass

class JWTAuthenticationStrategy(AuthenticationStrategy):
    def authenticate(self, credentials: dict) -> Optional[User]:
        # Implementación JWT
        pass

class BasicAuthenticationStrategy(AuthenticationStrategy):
    def authenticate(self, credentials: dict) -> Optional[User]:
        # Implementación Basic Auth
        pass
```

### 2. Command Pattern
**Propósito**: Encapsular operaciones como objetos

```python
class CreateUserCommand:
    def __init__(self, email: str, password: str):
        self.email = email
        self.password = password

class CreateUserHandler:
    def __init__(self, user_service: UserService):
        self.user_service = user_service
    
    def handle(self, command: CreateUserCommand) -> User:
        return self.user_service.create_user(command.email, command.password)
```

### 3. Template Method Pattern
**Propósito**: Definir esqueleto de algoritmo

```python
class BaseService(ABC):
    def process_request(self, data: dict) -> dict:
        self.validate_input(data)
        result = self.execute_business_logic(data)
        self.log_operation(result)
        return result
    
    @abstractmethod
    def execute_business_logic(self, data: dict) -> dict:
        pass
    
    def validate_input(self, data: dict) -> None:
        # Validación común
        pass
    
    def log_operation(self, result: dict) -> None:
        # Logging común
        pass
```

## Patrones de Integración

### 1. Adapter Pattern
**Propósito**: Adaptar interfaces incompatibles

```python
class YiqiERPAdapter:
    def __init__(self, yiqi_client: YiqiClient):
        self.client = yiqi_client
    
    def create_invoice(self, invoice_data: dict) -> Invoice:
        # Adaptar datos al formato de YiQi
        yiqi_format = self._convert_to_yiqi_format(invoice_data)
        response = self.client.create_invoice(yiqi_format)
        # Adaptar respuesta al formato interno
        return self._convert_from_yiqi_format(response)
```

### 2. Facade Pattern
**Propósito**: Simplificar interfaces complejas

```python
class UserManagementFacade:
    def __init__(self):
        self.user_service = service_locator.get_service("user_service")
        self.auth_service = service_locator.get_service("auth_service")
        self.rbac_service = service_locator.get_service("rbac_service")
    
    def create_user_with_role(self, email: str, password: str, role: str) -> User:
        # Operación compleja simplificada
        user = self.user_service.create_user(email, password)
        self.rbac_service.assign_role(user.id, role)
        token = self.auth_service.generate_token(user)
        return user
```

## Beneficios de los Patrones

### 1. **Mantenibilidad**
- Código organizado y predecible
- Separación clara de responsabilidades
- Fácil localización de cambios

### 2. **Extensibilidad**
- Nuevas funcionalidades sin modificar código existente
- Intercambio de implementaciones
- Evolución gradual del sistema

### 3. **Testabilidad**
- Mocking sencillo con interfaces
- Tests unitarios independientes
- Cobertura completa por capa

### 4. **Reutilización**
- Componentes intercambiables
- Patrones aplicables en múltiples contextos
- Reducción de duplicación de código