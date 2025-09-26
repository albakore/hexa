# Principios de Arquitectura Hexagonal

## Definición

La arquitectura hexagonal (también conocida como Ports & Adapters) es un patrón arquitectónico que busca aislar la lógica de negocio de las dependencias externas.

## Estructura por Capas

### 1. Dominio (Centro)
```
domain/
├── entity/          # Entidades de negocio
├── repository/      # Interfaces de repositorio
├── usecase/         # Casos de uso
├── vo/             # Value Objects
└── exception/      # Excepciones de dominio
```

**Responsabilidades:**
- Lógica de negocio pura
- Reglas de dominio
- Entidades y value objects
- Casos de uso

### 2. Aplicación (Intermedia)
```
application/
├── service/        # Servicios de aplicación
├── dto/           # Data Transfer Objects
└── exception/     # Excepciones de aplicación
```

**Responsabilidades:**
- Orquestación de casos de uso
- Transformación de datos
- Validaciones de aplicación
- Coordinación entre dominios

### 3. Adaptadores (Externa)
```
adapter/
├── input/
│   └── api/       # Controladores REST
└── output/
    └── persistence/ # Repositorios concretos
```

**Responsabilidades:**
- Comunicación con el exterior
- Implementación de interfaces
- Transformación de datos externos
- Integración con servicios externos

## Principios Fundamentales

### 1. Inversión de Dependencias
```python
# ❌ Dependencia directa
class UserService:
    def __init__(self):
        self.repository = MySQLUserRepository()

# ✅ Inversión de dependencias
class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository
```

### 2. Separación de Responsabilidades
- **Dominio**: QUÉ hace el sistema
- **Aplicación**: CÓMO se coordina
- **Adaptadores**: DÓNDE se conecta

### 3. Testabilidad
```python
# Test unitario del dominio
def test_user_creation():
    mock_repo = Mock(spec=UserRepository)
    service = UserService(mock_repo)
    
    user = service.create_user("test@example.com")
    
    assert user.email == "test@example.com"
    mock_repo.save.assert_called_once()
```

## Beneficios

### 1. **Mantenibilidad**
- Código organizado por responsabilidades
- Cambios localizados
- Fácil refactoring

### 2. **Testabilidad**
- Testing independiente por capa
- Mocking sencillo
- Tests rápidos y confiables

### 3. **Flexibilidad**
- Intercambio de adaptadores
- Múltiples interfaces
- Evolución independiente

### 4. **Escalabilidad**
- Separación clara de concerns
- Paralelización de desarrollo
- Microservicios ready

## Implementación en el Proyecto

### Estructura de Módulo
```
modules/user/
├── domain/
│   ├── entity/user.py
│   ├── repository/user.py
│   └── usecase/user.py
├── application/
│   ├── service/user.py
│   └── dto/user.py
├── adapter/
│   ├── input/api/v1/user.py
│   └── output/persistence/sqlalchemy/user.py
├── container.py
└── module.py
```

### Flujo de Datos
```
HTTP Request → Controller → Service → UseCase → Repository → Database
     ↑            ↓          ↓         ↓          ↓         ↓
   Adapter    Application  Domain   Domain   Adapter   External
```

## Reglas de Dependencia

1. **Dominio** no depende de nada
2. **Aplicación** depende solo del dominio
3. **Adaptadores** dependen de aplicación y dominio
4. **Nunca** dependencias hacia adentro desde capas externas