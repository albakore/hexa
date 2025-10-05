# Arquitectura del Proyecto

## Visión General

El proyecto implementa una **arquitectura hexagonal modular** que combina los principios de:

- **Hexagonal Architecture (Ports & Adapters)**
- **Modular Monolith**
- **Dependency Injection**
- **Service Locator Pattern**

## Diagrama de Arquitectura

```mermaid
graph TB
    subgraph "FastAPI Application"
        subgraph "Core Layer"
            Server[FastAPI Server]
            Config[Configuration]
            Middleware[Middlewares]
        end
        
        subgraph "Module Discovery"
            Discovery[Module Discovery]
            Registry[Module Registry]
            ServiceLocator[Service Locator]
        end
        
        subgraph "Modules"
            subgraph "User Module"
                UserAPI[User API]
                UserService[User Service]
                UserRepo[User Repository]
                UserDB[(User DB)]
            end
            
            subgraph "Auth Module"
                AuthAPI[Auth API]
                AuthService[Auth Service]
                AuthRepo[Auth Repository]
                Redis[(Redis)]
            end
            
            subgraph "RBAC Module"
                RBACService[RBAC Service]
                RoleRepo[Role Repository]
                PermRepo[Permission Repository]
            end
        end
        
        subgraph "Shared Layer"
            Interfaces[Interfaces]
            Models[Shared Models]
            Utils[Utilities]
        end
    end
    
    subgraph "External"
        DB[(PostgreSQL)]
        Cache[(Redis)]
        Client[API Client]
    end
    
    Client --> Server
    Server --> Discovery
    Discovery --> Registry
    Registry --> ServiceLocator
    
    UserAPI --> UserService
    UserService --> UserRepo
    UserRepo --> UserDB
    
    AuthAPI --> AuthService
    AuthService --> AuthRepo
    AuthRepo --> Redis
    
    UserService -.-> ServiceLocator
    AuthService -.-> ServiceLocator
    RBACService -.-> ServiceLocator
    
    UserDB --> DB
    Redis --> Cache
```

## Capas de la Arquitectura

### 1. Core Layer
**Responsabilidad**: Configuración central y servidor FastAPI

```
core/
├── config/          # Configuración de la aplicación
├── db/             # Configuración de base de datos
├── exceptions/     # Excepciones personalizadas
└── fastapi/        # Configuración de FastAPI
    ├── dependencies/
    ├── middlewares/
    └── server/
```

### 2. Module Layer
**Responsabilidad**: Lógica de negocio modular

Cada módulo sigue la estructura hexagonal:

```
modules/[module_name]/
├── adapter/
│   ├── input/      # Controladores (API, CLI, etc.)
│   └── output/     # Repositorios, APIs externas
├── application/    # Casos de uso y servicios
├── domain/         # Entidades y lógica de dominio
├── container.py    # Inyección de dependencias
└── module.py       # Definición del módulo
```

### 3. Shared Layer
**Responsabilidad**: Interfaces y utilidades compartidas

```
shared/
├── interfaces/     # Contratos entre módulos
├── models.py       # Modelos compartidos
└── dependencies.py # Dependencias globales
```

## Principios Arquitectónicos

### 1. Separación de Responsabilidades

- **Domain**: Lógica de negocio pura
- **Application**: Casos de uso y orquestación
- **Infrastructure**: Detalles técnicos (DB, API, etc.)

### 2. Inversión de Dependencias

```python
# ✅ Correcto - Depende de abstracción
class UserService:
    def __init__(self, repository: UserRepositoryInterface):
        self.repository = repository

# ❌ Incorrecto - Depende de implementación concreta
class UserService:
    def __init__(self):
        self.repository = SQLUserRepository()
```

### 3. Modularidad

Cada módulo es:
- **Independiente**: Puede funcionar por sí solo
- **Portable**: Se puede extraer fácilmente
- **Testeable**: Dependencias mockeables

### 4. Comunicación entre Módulos

```python
# Comunicación a través del Service Locator
role_service = service_locator.get_service("rbac.role_service")
user_roles = role_service.get_user_roles(user_id)
```

## Flujo de Datos

### 1. Inicialización
```mermaid
sequenceDiagram
    participant App as FastAPI App
    participant Discovery as Module Discovery
    participant Registry as Module Registry
    participant Locator as Service Locator
    participant Module as User Module
    
    App->>Discovery: discover_modules()
    Discovery->>Module: import module.py
    Module->>Registry: register(UserModule)
    Module->>Locator: register_service("user_service", service)
    Registry->>App: return routes
```

### 2. Request Processing
```mermaid
sequenceDiagram
    participant Client
    participant API as FastAPI Route
    participant Service as User Service
    participant Repo as User Repository
    participant DB as Database
    
    Client->>API: POST /users
    API->>Service: create_user(command)
    Service->>Repo: save(user)
    Repo->>DB: INSERT user
    DB-->>Repo: user_id
    Repo-->>Service: User entity
    Service-->>API: UserResponse
    API-->>Client: 201 Created
```

## Patrones Utilizados

### 1. Repository Pattern
Abstrae el acceso a datos

### 2. Service Layer Pattern
Encapsula la lógica de negocio

### 3. Dependency Injection
Gestiona dependencias automáticamente

### 4. Service Locator
Permite comunicación entre módulos

### 5. Module Pattern
Organiza funcionalidades en módulos cohesivos

## Ventajas de esta Arquitectura

- ✅ **Testabilidad**: Fácil mockear dependencias
- ✅ **Mantenibilidad**: Código organizado y separado
- ✅ **Escalabilidad**: Fácil agregar nuevos módulos
- ✅ **Flexibilidad**: Cambiar implementaciones sin afectar otros módulos
- ✅ **Reutilización**: Módulos portables entre proyectos