# Módulos del Sistema

Los módulos del sistema proporcionan funcionalidades core necesarias para el funcionamiento básico de la aplicación.

## 🔐 Auth Module

**Ubicación**: `modules/auth/`
**Propósito**: Autenticación y gestión de tokens JWT

### Funcionalidades
- Autenticación de usuarios
- Generación y validación de tokens JWT
- Gestión de sesiones
- Refresh tokens

### Componentes Principales

#### Domain
```python
# domain/usecase/auth.py
class AuthenticateUserUseCase:
    def execute(self, email: str, password: str) -> Optional[User]:
        user = self.user_repository.find_by_email(email)
        if user and self._verify_password(password, user.password_hash):
            return user
        return None

# domain/usecase/jwt.py
class GenerateTokenUseCase:
    def execute(self, user: User) -> TokenPair:
        access_token = self._create_access_token(user)
        refresh_token = self._create_refresh_token(user)
        return TokenPair(access_token, refresh_token)
```

#### Application
```python
# application/service/auth.py
class AuthService:
    def authenticate(self, email: str, password: str) -> Optional[AuthTokenDTO]:
        user = self.auth_usecase.execute(email, password)
        if user:
            tokens = self.jwt_usecase.execute(user)
            return AuthTokenDTO.from_tokens(tokens)
        return None
```

#### Endpoints
- `POST /auth/login` - Autenticación
- `POST /auth/refresh` - Renovar token
- `POST /auth/logout` - Cerrar sesión

---

## 👤 User Module

**Ubicación**: `modules/user/`
**Propósito**: Gestión de usuarios del sistema

### Funcionalidades
- CRUD de usuarios
- Gestión de perfiles
- Validación de datos
- Historial de actividad

### Componentes Principales

#### Domain
```python
# domain/entity/user.py
class User:
    def __init__(self, email: str, password: str):
        self.email = self._validate_email(email)
        self.password_hash = self._hash_password(password)
        self.is_active = True
        self.created_at = datetime.now()
    
    def deactivate(self) -> None:
        self.is_active = False
    
    def change_password(self, new_password: str) -> None:
        self.password_hash = self._hash_password(new_password)

# domain/usecase/user.py
class CreateUserUseCase:
    def execute(self, email: str, password: str) -> User:
        if self.repository.find_by_email(email):
            raise UserAlreadyExistsError()
        
        user = User(email, password)
        return self.repository.save(user)
```

#### Application
```python
# application/service/user.py
class UserService:
    def create_user(self, email: str, password: str) -> UserDTO:
        user = self.create_user_usecase.execute(email, password)
        
        # Publicar evento
        event = DomainEvent(
            event_type="user_created",
            data={"user_id": user.id, "email": email},
            timestamp=datetime.now(),
            module_source="user"
        )
        event_bus.publish(event)
        
        return UserDTO.from_entity(user)
```

#### Endpoints
- `GET /users` - Listar usuarios
- `POST /users` - Crear usuario
- `GET /users/{id}` - Obtener usuario
- `PUT /users/{id}` - Actualizar usuario
- `DELETE /users/{id}` - Eliminar usuario

---

## 🛡️ RBAC Module

**Ubicación**: `modules/rbac/`
**Propósito**: Control de acceso basado en roles

### Funcionalidades
- Gestión de roles
- Gestión de permisos
- Asignación de roles a usuarios
- Verificación de permisos

### Componentes Principales

#### Domain
```python
# domain/entity/role.py
class Role:
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.permissions: List[Permission] = []
    
    def add_permission(self, permission: Permission) -> None:
        if permission not in self.permissions:
            self.permissions.append(permission)

# domain/entity/permission.py
class Permission:
    def __init__(self, name: str, resource: str, action: str):
        self.name = name
        self.resource = resource
        self.action = action
```

#### Application
```python
# application/service/role.py
class RoleService:
    def create_role(self, name: str, description: str) -> RoleDTO:
        role = Role(name, description)
        saved_role = self.repository.save(role)
        return RoleDTO.from_entity(saved_role)
    
    def assign_role_to_user(self, user_id: int, role_id: int) -> None:
        self.repository.assign_role(user_id, role_id)
```

#### Endpoints
- `GET /rbac/roles` - Listar roles
- `POST /rbac/roles` - Crear rol
- `GET /rbac/permissions` - Listar permisos
- `POST /rbac/users/{id}/roles` - Asignar rol

---

## 🔗 User Relationships Module

**Ubicación**: `modules/user_relationships/`
**Propósito**: Gestión de relaciones entre entidades

### Funcionalidades
- Relaciones entre usuarios
- Jerarquías organizacionales
- Grupos y equipos
- Seguimiento de relaciones

### Componentes Principales

#### Domain
```python
# domain/entity.py
class UserRelationship:
    def __init__(self, from_user_id: int, to_user_id: int, relationship_type: str):
        self.from_user_id = from_user_id
        self.to_user_id = to_user_id
        self.relationship_type = relationship_type
        self.created_at = datetime.now()
        self.is_active = True
```

#### Application
```python
# application/service.py
class UserRelationshipService:
    def create_relationship(self, from_user_id: int, to_user_id: int, 
                          relationship_type: str) -> UserRelationshipDTO:
        relationship = UserRelationship(from_user_id, to_user_id, relationship_type)
        saved = self.repository.save(relationship)
        return UserRelationshipDTO.from_entity(saved)
```

#### Endpoints
- `GET /user-relationships` - Listar relaciones
- `POST /user-relationships` - Crear relación
- `DELETE /user-relationships/{id}` - Eliminar relación

---

## 📦 App Module Module

**Ubicación**: `modules/app_module/`
**Propósito**: Gestión de módulos de aplicación

### Funcionalidades
- Registro de módulos
- Configuración de módulos
- Estado de módulos
- Dependencias entre módulos

### Componentes Principales

#### Domain
```python
# domain/entity/module.py
class AppModule:
    def __init__(self, name: str, version: str, description: str):
        self.name = name
        self.version = version
        self.description = description
        self.is_enabled = True
        self.dependencies: List[str] = []
```

#### Application
```python
# application/service/module.py
class AppModuleService:
    def register_module(self, name: str, version: str, description: str) -> AppModuleDTO:
        module = AppModule(name, version, description)
        saved = self.repository.save(module)
        return AppModuleDTO.from_entity(saved)
```

#### Endpoints
- `GET /modules` - Listar módulos
- `POST /modules` - Registrar módulo
- `PUT /modules/{id}/enable` - Habilitar módulo
- `PUT /modules/{id}/disable` - Deshabilitar módulo

## Comunicación Entre Módulos del Sistema

### Event-Driven Communication
```python
# Ejemplo: User creado → Auth genera token inicial
class AuthUserCreatedHandler(EventHandler):
    def handle(self, event: DomainEvent) -> None:
        if event.event_type == "user_created":
            user_id = event.data["user_id"]
            # Generar token inicial o configurar auth
            self.setup_initial_auth(user_id)

# Registro del handler
event_bus.subscribe("user_created", AuthUserCreatedHandler())
```

### Service Locator
```python
# Auth module necesita validar usuario
class AuthService:
    def __init__(self):
        self.user_service = service_locator.get_service("user_service")
    
    def authenticate(self, email: str, password: str) -> Optional[AuthTokenDTO]:
        user = self.user_service.get_by_email(email)
        if user and self._verify_password(password, user.password_hash):
            return self._generate_tokens(user)
        return None
```

## Configuración y Despliegue

### Health Checks por Módulo
```python
@router.get("/health")
async def module_health():
    return {
        "module": "auth",
        "status": "healthy",
        "dependencies": ["user", "rbac"],
        "version": "1.0.0"
    }
```

### Métricas
```python
@router.get("/metrics")
async def module_metrics():
    return {
        "module": "user",
        "active_users": get_active_user_count(),
        "requests_per_minute": get_rpm(),
        "average_response_time": get_avg_response_time()
    }
```