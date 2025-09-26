# Comunicación Entre Módulos

## Principios de Comunicación

La comunicación entre módulos sigue principios de desacoplamiento, utilizando patrones que evitan dependencias directas y mantienen la independencia de cada módulo.

## Patrones de Comunicación

### 1. Service Locator Pattern
### 2. Event-Driven Communication
### 3. Shared Interfaces
### 4. Message Passing

## Service Locator Pattern

### Implementación del Service Locator
```python
# shared/interfaces/service_locator.py
from typing import Dict, Any, Optional, TypeVar, Type, Callable
from abc import ABC, abstractmethod
import logging

T = TypeVar('T')
logger = logging.getLogger(__name__)

class ServiceLocator:
    """Localizador de servicios para comunicación entre módulos"""
    
    def __init__(self):
        self._services: Dict[str, Any] = {}
        self._factories: Dict[str, Callable] = {}
        self._singletons: Dict[str, Any] = {}
    
    def register_service(self, name: str, service: Any) -> None:
        """Registra un servicio por nombre"""
        self._services[name] = service
        logger.debug(f"Service registered: {name}")
    
    def register_factory(self, name: str, factory: Callable) -> None:
        """Registra una factory para crear servicios bajo demanda"""
        self._factories[name] = factory
        logger.debug(f"Factory registered: {name}")
    
    def register_singleton_factory(self, name: str, factory: Callable) -> None:
        """Registra una factory que produce singletons"""
        self._factories[name] = factory
        logger.debug(f"Singleton factory registered: {name}")
    
    def get_service(self, name: str) -> Optional[Any]:
        """Obtiene un servicio por nombre"""
        # Verificar servicios directos
        if name in self._services:
            return self._services[name]
        
        # Verificar singletons
        if name in self._singletons:
            return self._singletons[name]
        
        # Crear desde factory
        if name in self._factories:
            service = self._factories[name]()
            
            # Si es singleton, guardarlo
            if name.endswith('_singleton') or name in self._singletons:
                self._singletons[name] = service
            
            return service
        
        logger.warning(f"Service not found: {name}")
        return None
    
    def get_typed_service(self, name: str, service_type: Type[T]) -> Optional[T]:
        """Obtiene un servicio tipado"""
        service = self.get_service(name)
        if service and isinstance(service, service_type):
            return service
        return None
    
    def has_service(self, name: str) -> bool:
        """Verifica si un servicio está disponible"""
        return (name in self._services or 
                name in self._factories or 
                name in self._singletons)
    
    def list_services(self) -> Dict[str, str]:
        """Lista todos los servicios disponibles"""
        services = {}
        
        for name in self._services:
            services[name] = "direct"
        
        for name in self._factories:
            services[name] = "factory"
        
        for name in self._singletons:
            services[name] = "singleton"
        
        return services
    
    def clear(self) -> None:
        """Limpia todos los servicios registrados"""
        self._services.clear()
        self._factories.clear()
        self._singletons.clear()

# Instancia global del localizador de servicios
service_locator = ServiceLocator()
```

### Uso del Service Locator
```python
# Ejemplo: Módulo Auth necesita UserService
# modules/auth/application/service/auth.py
from shared.interfaces.service_locator import service_locator

class AuthService:
    def __init__(self):
        # Obtener servicio de usuario sin dependencia directa
        self._user_service = None
    
    @property
    def user_service(self):
        """Lazy loading del servicio de usuario"""
        if self._user_service is None:
            self._user_service = service_locator.get_service("user_service")
        return self._user_service
    
    def authenticate(self, email: str, password: str) -> Optional[AuthTokenDTO]:
        """Autenticar usuario"""
        if not self.user_service:
            raise ServiceNotAvailableError("User service not available")
        
        # Usar servicio de usuario
        user = self.user_service.get_by_email(email)
        if user and self._verify_password(password, user.password_hash):
            return self._generate_tokens(user)
        
        return None

# Registro del servicio en el módulo
# modules/user/module.py
class UserModule(ModuleInterface):
    def initialize(self) -> None:
        # Registrar servicio para que otros módulos lo usen
        service_locator.register_service("user_service", self.container.service())
```

## Event-Driven Communication

### Sistema de Eventos
```python
# shared/interfaces/events.py
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Callable
from dataclasses import dataclass
from datetime import datetime
import asyncio
import logging

logger = logging.getLogger(__name__)

@dataclass
class DomainEvent:
    """Evento de dominio base"""
    event_type: str
    data: Dict[str, Any]
    timestamp: datetime
    module_source: str
    correlation_id: str = None
    
    def __post_init__(self):
        if self.correlation_id is None:
            import uuid
            self.correlation_id = str(uuid.uuid4())

class EventHandler(ABC):
    """Interface para manejadores de eventos"""
    
    @abstractmethod
    async def handle(self, event: DomainEvent) -> None:
        """Maneja un evento de dominio"""
        pass
    
    @property
    def handler_name(self) -> str:
        """Nombre del handler para logging"""
        return self.__class__.__name__

class EventBus:
    """Bus de eventos para comunicación asíncrona entre módulos"""
    
    def __init__(self):
        self._handlers: Dict[str, List[EventHandler]] = {}
        self._async_handlers: Dict[str, List[EventHandler]] = {}
        self._middleware: List[Callable] = []
    
    def subscribe(self, event_type: str, handler: EventHandler, async_handler: bool = False) -> None:
        """Suscribe un handler a un tipo de evento"""
        handlers_dict = self._async_handlers if async_handler else self._handlers
        
        if event_type not in handlers_dict:
            handlers_dict[event_type] = []
        
        handlers_dict[event_type].append(handler)
        logger.info(f"Handler {handler.handler_name} subscribed to {event_type}")
    
    def unsubscribe(self, event_type: str, handler: EventHandler) -> None:
        """Desuscribe un handler de un tipo de evento"""
        for handlers_dict in [self._handlers, self._async_handlers]:
            if event_type in handlers_dict:
                if handler in handlers_dict[event_type]:
                    handlers_dict[event_type].remove(handler)
                    logger.info(f"Handler {handler.handler_name} unsubscribed from {event_type}")
    
    def add_middleware(self, middleware: Callable) -> None:
        """Agregar middleware para procesamiento de eventos"""
        self._middleware.append(middleware)
    
    async def publish(self, event: DomainEvent) -> None:
        """Publica un evento a todos los handlers suscritos"""
        logger.info(f"Publishing event {event.event_type} from {event.module_source}")
        
        # Aplicar middleware
        for middleware in self._middleware:
            event = await middleware(event)
            if event is None:
                return
        
        # Handlers síncronos
        sync_handlers = self._handlers.get(event.event_type, [])
        for handler in sync_handlers:
            try:
                await handler.handle(event)
                logger.debug(f"Event handled by {handler.handler_name}")
            except Exception as e:
                logger.error(f"Error in handler {handler.handler_name}: {e}")
        
        # Handlers asíncronos (ejecutar en paralelo)
        async_handlers = self._async_handlers.get(event.event_type, [])
        if async_handlers:
            tasks = []
            for handler in async_handlers:
                task = asyncio.create_task(self._handle_async(handler, event))
                tasks.append(task)
            
            # Esperar a que todos terminen
            await asyncio.gather(*tasks, return_exceptions=True)
    
    async def _handle_async(self, handler: EventHandler, event: DomainEvent) -> None:
        """Manejar evento asíncrono con logging de errores"""
        try:
            await handler.handle(event)
            logger.debug(f"Async event handled by {handler.handler_name}")
        except Exception as e:
            logger.error(f"Error in async handler {handler.handler_name}: {e}")
    
    def get_subscribers(self, event_type: str) -> List[str]:
        """Obtener lista de suscriptores para un tipo de evento"""
        subscribers = []
        
        for handler in self._handlers.get(event_type, []):
            subscribers.append(f"{handler.handler_name} (sync)")
        
        for handler in self._async_handlers.get(event_type, []):
            subscribers.append(f"{handler.handler_name} (async)")
        
        return subscribers

# Instancia global del bus de eventos
event_bus = EventBus()
```

### Implementación de Event Handlers
```python
# Ejemplo: Handler para eventos de usuario
# modules/auth/application/event_handlers/user_handlers.py
from shared.interfaces.events import EventHandler, DomainEvent
from shared.interfaces.service_locator import service_locator

class UserCreatedHandler(EventHandler):
    """Handler para cuando se crea un usuario"""
    
    async def handle(self, event: DomainEvent) -> None:
        if event.event_type != "user_created":
            return
        
        user_id = event.data.get("user_id")
        email = event.data.get("email")
        
        # Crear sesión inicial para el usuario
        auth_service = service_locator.get_service("auth_service")
        if auth_service:
            await auth_service.create_initial_session(user_id)
        
        # Log del evento
        logger.info(f"Created initial auth session for user {user_id}")

class UserDeactivatedHandler(EventHandler):
    """Handler para cuando se desactiva un usuario"""
    
    async def handle(self, event: DomainEvent) -> None:
        if event.event_type != "user_deactivated":
            return
        
        user_id = event.data.get("user_id")
        
        # Invalidar todas las sesiones del usuario
        auth_service = service_locator.get_service("auth_service")
        if auth_service:
            await auth_service.invalidate_user_sessions(user_id)
        
        logger.info(f"Invalidated all sessions for deactivated user {user_id}")

# Registro de handlers en el módulo
# modules/auth/module.py
class AuthModule(ModuleInterface):
    def initialize(self) -> None:
        # Suscribirse a eventos de usuario
        from modules.auth.application.event_handlers.user_handlers import (
            UserCreatedHandler, UserDeactivatedHandler
        )
        
        event_bus.subscribe("user_created", UserCreatedHandler())
        event_bus.subscribe("user_deactivated", UserDeactivatedHandler())
```

### Publicación de Eventos
```python
# Ejemplo: Publicar evento desde módulo de usuario
# modules/user/application/service/user.py
from shared.interfaces.events import event_bus, DomainEvent
from datetime import datetime

class UserService:
    async def create_user(self, email: str, password: str) -> UserDTO:
        """Crear usuario y publicar evento"""
        user = self.create_user_usecase.execute(email, password)
        
        # Publicar evento
        event = DomainEvent(
            event_type="user_created",
            data={
                "user_id": user.id,
                "email": user.email,
                "created_at": user.created_at.isoformat()
            },
            timestamp=datetime.now(),
            module_source="user"
        )
        
        await event_bus.publish(event)
        
        return UserDTO.from_entity(user)
    
    async def deactivate_user(self, user_id: int) -> None:
        """Desactivar usuario y publicar evento"""
        user = self.deactivate_user_usecase.execute(user_id)
        
        # Publicar evento
        event = DomainEvent(
            event_type="user_deactivated",
            data={
                "user_id": user.id,
                "email": user.email,
                "deactivated_at": datetime.now().isoformat()
            },
            timestamp=datetime.now(),
            module_source="user"
        )
        
        await event_bus.publish(event)
```

## Shared Interfaces

### Definición de Interfaces Compartidas
```python
# shared/interfaces/user_interface.py
from abc import ABC, abstractmethod
from typing import Optional, List
from dataclasses import dataclass

@dataclass
class UserInfo:
    """Información básica de usuario compartida entre módulos"""
    id: int
    email: str
    is_active: bool
    created_at: str

class UserServiceInterface(ABC):
    """Interface compartida para servicios de usuario"""
    
    @abstractmethod
    async def get_user_by_id(self, user_id: int) -> Optional[UserInfo]:
        """Obtener usuario por ID"""
        pass
    
    @abstractmethod
    async def get_user_by_email(self, email: str) -> Optional[UserInfo]:
        """Obtener usuario por email"""
        pass
    
    @abstractmethod
    async def is_user_active(self, user_id: int) -> bool:
        """Verificar si un usuario está activo"""
        pass
    
    @abstractmethod
    async def get_users_by_ids(self, user_ids: List[int]) -> List[UserInfo]:
        """Obtener múltiples usuarios por IDs"""
        pass

# shared/interfaces/auth_interface.py
@dataclass
class AuthInfo:
    """Información de autenticación compartida"""
    user_id: int
    token: str
    expires_at: str

class AuthServiceInterface(ABC):
    """Interface compartida para servicios de autenticación"""
    
    @abstractmethod
    async def validate_token(self, token: str) -> Optional[AuthInfo]:
        """Validar token de autenticación"""
        pass
    
    @abstractmethod
    async def get_user_permissions(self, user_id: int) -> List[str]:
        """Obtener permisos de un usuario"""
        pass
```

### Implementación de Interfaces
```python
# modules/user/adapter/interface/user_service_adapter.py
from shared.interfaces.user_interface import UserServiceInterface, UserInfo
from modules.user.application.service.user import UserService

class UserServiceAdapter(UserServiceInterface):
    """Adaptador que implementa la interface compartida"""
    
    def __init__(self, user_service: UserService):
        self.user_service = user_service
    
    async def get_user_by_id(self, user_id: int) -> Optional[UserInfo]:
        user_dto = await self.user_service.get_user_by_id(user_id)
        if not user_dto:
            return None
        
        return UserInfo(
            id=user_dto.id,
            email=user_dto.email,
            is_active=user_dto.is_active,
            created_at=user_dto.created_at.isoformat()
        )
    
    async def get_user_by_email(self, email: str) -> Optional[UserInfo]:
        user_dto = await self.user_service.get_by_email(email)
        if not user_dto:
            return None
        
        return UserInfo(
            id=user_dto.id,
            email=user_dto.email,
            is_active=user_dto.is_active,
            created_at=user_dto.created_at.isoformat()
        )
    
    async def is_user_active(self, user_id: int) -> bool:
        user = await self.get_user_by_id(user_id)
        return user.is_active if user else False
    
    async def get_users_by_ids(self, user_ids: List[int]) -> List[UserInfo]:
        users = []
        for user_id in user_ids:
            user = await self.get_user_by_id(user_id)
            if user:
                users.append(user)
        return users

# Registro del adaptador
# modules/user/module.py
class UserModule(ModuleInterface):
    def initialize(self) -> None:
        # Registrar adaptador de interface
        user_adapter = UserServiceAdapter(self.container.service())
        service_locator.register_service("user_interface", user_adapter)
```

## Message Passing

### Sistema de Mensajes
```python
# shared/interfaces/message_bus.py
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Callable
from dataclasses import dataclass
from datetime import datetime
import asyncio
import json
import logging

logger = logging.getLogger(__name__)

@dataclass
class Message:
    """Mensaje entre módulos"""
    type: str
    payload: Dict[str, Any]
    sender: str
    recipient: str
    timestamp: datetime
    correlation_id: str = None
    reply_to: str = None
    
    def __post_init__(self):
        if self.correlation_id is None:
            import uuid
            self.correlation_id = str(uuid.uuid4())

class MessageHandler(ABC):
    """Interface para manejadores de mensajes"""
    
    @abstractmethod
    async def handle_message(self, message: Message) -> Optional[Message]:
        """Maneja un mensaje y opcionalmente retorna una respuesta"""
        pass

class MessageBus:
    """Bus de mensajes para comunicación directa entre módulos"""
    
    def __init__(self):
        self._handlers: Dict[str, Dict[str, MessageHandler]] = {}
        self._pending_replies: Dict[str, asyncio.Future] = {}
    
    def register_handler(self, module_name: str, message_type: str, handler: MessageHandler) -> None:
        """Registrar handler para un tipo de mensaje"""
        if module_name not in self._handlers:
            self._handlers[module_name] = {}
        
        self._handlers[module_name][message_type] = handler
        logger.info(f"Message handler registered: {module_name}.{message_type}")
    
    async def send_message(self, message: Message) -> None:
        """Enviar mensaje sin esperar respuesta"""
        await self._route_message(message)
    
    async def send_request(self, message: Message, timeout: float = 30.0) -> Optional[Message]:
        """Enviar mensaje y esperar respuesta"""
        # Configurar para esperar respuesta
        future = asyncio.Future()
        self._pending_replies[message.correlation_id] = future
        
        # Enviar mensaje
        await self._route_message(message)
        
        try:
            # Esperar respuesta con timeout
            response = await asyncio.wait_for(future, timeout=timeout)
            return response
        except asyncio.TimeoutError:
            logger.warning(f"Message timeout: {message.type} to {message.recipient}")
            return None
        finally:
            # Limpiar
            self._pending_replies.pop(message.correlation_id, None)
    
    async def _route_message(self, message: Message) -> None:
        """Enrutar mensaje al handler apropiado"""
        recipient_handlers = self._handlers.get(message.recipient, {})
        handler = recipient_handlers.get(message.type)
        
        if not handler:
            logger.warning(f"No handler found for {message.recipient}.{message.type}")
            return
        
        try:
            response = await handler.handle_message(message)
            
            # Si hay respuesta y el mensaje original esperaba una
            if response and message.reply_to:
                response.recipient = message.reply_to
                response.correlation_id = message.correlation_id
                
                # Si hay un future esperando, resolverlo
                if message.correlation_id in self._pending_replies:
                    future = self._pending_replies[message.correlation_id]
                    if not future.done():
                        future.set_result(response)
                else:
                    # Enviar respuesta como mensaje normal
                    await self._route_message(response)
            
        except Exception as e:
            logger.error(f"Error handling message {message.type}: {e}")

# Instancia global del bus de mensajes
message_bus = MessageBus()
```

### Uso del Message Bus
```python
# Ejemplo: Comunicación entre módulos Finance y Provider
# modules/finance/application/message_handlers/provider_handlers.py
from shared.interfaces.message_bus import MessageHandler, Message

class ProviderValidationHandler(MessageHandler):
    """Handler para validar información de proveedores"""
    
    def __init__(self, finance_service):
        self.finance_service = finance_service
    
    async def handle_message(self, message: Message) -> Optional[Message]:
        if message.type != "validate_provider_financial_info":
            return None
        
        provider_id = message.payload.get("provider_id")
        
        # Validar información financiera del proveedor
        is_valid = await self.finance_service.validate_provider(provider_id)
        
        # Retornar respuesta
        return Message(
            type="provider_validation_response",
            payload={"provider_id": provider_id, "is_valid": is_valid},
            sender="finance",
            recipient=message.sender,
            timestamp=datetime.now(),
            reply_to=message.sender
        )

# Registro del handler
# modules/finance/module.py
class FinanceModule(ModuleInterface):
    def initialize(self) -> None:
        handler = ProviderValidationHandler(self.container.service())
        message_bus.register_handler("finance", "validate_provider_financial_info", handler)

# Uso desde otro módulo
# modules/provider/application/service/provider.py
from shared.interfaces.message_bus import message_bus, Message

class ProviderService:
    async def create_provider(self, provider_data: dict) -> ProviderDTO:
        # Crear proveedor
        provider = self.create_provider_usecase.execute(provider_data)
        
        # Validar información financiera
        validation_message = Message(
            type="validate_provider_financial_info",
            payload={"provider_id": provider.id},
            sender="provider",
            recipient="finance",
            timestamp=datetime.now(),
            reply_to="provider"
        )
        
        response = await message_bus.send_request(validation_message)
        
        if response and not response.payload.get("is_valid"):
            # Manejar validación fallida
            logger.warning(f"Financial validation failed for provider {provider.id}")
        
        return ProviderDTO.from_entity(provider)
```

## Middleware de Comunicación

### Event Middleware
```python
# shared/interfaces/event_middleware.py
from shared.interfaces.events import DomainEvent
import logging

logger = logging.getLogger(__name__)

async def logging_middleware(event: DomainEvent) -> DomainEvent:
    """Middleware para logging de eventos"""
    logger.info(f"Event: {event.event_type} from {event.module_source} at {event.timestamp}")
    return event

async def validation_middleware(event: DomainEvent) -> Optional[DomainEvent]:
    """Middleware para validación de eventos"""
    if not event.event_type or not event.module_source:
        logger.error("Invalid event: missing required fields")
        return None
    
    return event

async def metrics_middleware(event: DomainEvent) -> DomainEvent:
    """Middleware para métricas de eventos"""
    # Incrementar contador de eventos
    from shared.metrics import event_counter
    event_counter.labels(
        event_type=event.event_type,
        module=event.module_source
    ).inc()
    
    return event

# Registro de middleware
event_bus.add_middleware(logging_middleware)
event_bus.add_middleware(validation_middleware)
event_bus.add_middleware(metrics_middleware)
```

## Monitoreo de Comunicación

### Health Checks de Comunicación
```python
# shared/interfaces/communication_health.py
from typing import Dict, List
import asyncio

class CommunicationHealthChecker:
    """Verificador de salud de comunicación entre módulos"""
    
    def __init__(self):
        self.service_locator = service_locator
        self.event_bus = event_bus
        self.message_bus = message_bus
    
    async def check_service_locator_health(self) -> Dict[str, Any]:
        """Verificar salud del service locator"""
        services = self.service_locator.list_services()
        
        health_status = {
            "status": "healthy",
            "total_services": len(services),
            "services": services
        }
        
        # Verificar algunos servicios críticos
        critical_services = ["user_service", "auth_service", "rbac_service"]
        missing_services = []
        
        for service_name in critical_services:
            if not self.service_locator.has_service(service_name):
                missing_services.append(service_name)
        
        if missing_services:
            health_status["status"] = "degraded"
            health_status["missing_critical_services"] = missing_services
        
        return health_status
    
    async def check_event_bus_health(self) -> Dict[str, Any]:
        """Verificar salud del event bus"""
        # Obtener estadísticas de suscriptores
        event_types = ["user_created", "user_updated", "auth_login", "auth_logout"]
        subscribers_info = {}
        
        for event_type in event_types:
            subscribers = self.event_bus.get_subscribers(event_type)
            subscribers_info[event_type] = subscribers
        
        return {
            "status": "healthy",
            "subscribers": subscribers_info,
            "total_event_types": len(subscribers_info)
        }
    
    async def test_communication_flow(self) -> Dict[str, Any]:
        """Probar flujo completo de comunicación"""
        test_results = {}
        
        # Test 1: Service Locator
        try:
            user_service = self.service_locator.get_service("user_service")
            test_results["service_locator"] = "ok" if user_service else "failed"
        except Exception as e:
            test_results["service_locator"] = f"error: {e}"
        
        # Test 2: Event Bus
        try:
            test_event = DomainEvent(
                event_type="health_check_test",
                data={"test": True},
                timestamp=datetime.now(),
                module_source="health_checker"
            )
            await self.event_bus.publish(test_event)
            test_results["event_bus"] = "ok"
        except Exception as e:
            test_results["event_bus"] = f"error: {e}"
        
        return test_results

# Endpoint de health check
@router.get("/health/communication")
async def communication_health():
    checker = CommunicationHealthChecker()
    
    return {
        "service_locator": await checker.check_service_locator_health(),
        "event_bus": await checker.check_event_bus_health(),
        "communication_test": await checker.test_communication_flow()
    }
```

La comunicación entre módulos mediante estos patrones garantiza el desacoplamiento mientras proporciona mecanismos robustos y flexibles para la interacción entre componentes del sistema.