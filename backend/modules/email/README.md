# Módulo Email

Módulo para envío de correos electrónicos con soporte SMTP y templates dinámicos.

## Características

- ✅ Envío de emails con SMTP nativo de Python
- ✅ Soporte para templates HTML dinámicos con Jinja2
- ✅ Archivos adjuntos
- ✅ CC y BCC
- ✅ Conexión segura SSL/TLS
- ✅ Envío en batch (múltiples emails)
- ✅ Arquitectura hexagonal desacoplada

## Estructura del Módulo

```
email/
├── domain/
│   ├── entity/
│   │   └── email.py              # Entidad Email y EmailAttachment
│   ├── repository/
│   │   └── email_repository.py   # Interface abstracta EmailRepository
│   └── exception/
│       └── email_exceptions.py   # Excepciones del dominio
├── adapter/
│   └── output/
│       ├── smtp_email_adapter.py # Implementación SMTP
│       └── email_adapter.py      # Wrapper del repositorio
├── application/
│   ├── dto/
│   │   └── email_dto.py          # Commands (SendEmailCommand, SendTemplateEmailCommand)
│   └── service/
│       └── email_service.py      # Servicio de aplicación
├── templates/
│   ├── welcome.html              # Template de bienvenida
│   ├── password_reset.html       # Template de reset de contraseña
│   └── notification.html         # Template de notificación genérica
├── container.py                  # Dependency Injection Container
└── module.py                     # Configuración del módulo
```

## Configuración

Las variables de entorno necesarias ya están definidas en `core/config/settings.py`:

```python
EMAIL_SMTP_SERVER=smtp.gmail.com
EMAIL_SMTP_PORT=587
EMAIL_SMTP_USERNAME=tu_email@gmail.com
EMAIL_SMTP_PASSWORD=tu_contraseña
EMAIL_SMTP_MAILSENDER=tu_email@gmail.com
EMAIL_SMTP_APPLICATION=Hexa Platform
```

## Uso

### 1. Envío de Email Simple

```python
from modules.email.application.dto import SendEmailCommand
from modules.email.container import EmailContainer

# Obtener el servicio
container = EmailContainer()
email_service = container.service()

# Crear comando
command = SendEmailCommand(
    to=["usuario@example.com"],
    subject="Bienvenido a la plataforma",
    body="<h1>Hola!</h1><p>Bienvenido a nuestra plataforma.</p>",
    is_html=True
)

# Enviar email
await email_service.send_email(command)
```

### 2. Envío con Template Dinámico

```python
from modules.email.application.dto import SendTemplateEmailCommand
from datetime import datetime

# Crear comando con datos dinámicos
command = SendTemplateEmailCommand(
    to=["usuario@example.com"],
    subject="Bienvenido a la plataforma",
    template_name="welcome.html",
    template_data={
        "user_name": "Juan Pérez",
        "user_email": "usuario@example.com",
        "company_name": "Empresa ABC",
        "activation_link": "https://plataforma.com/activate/token123",
        "app_name": "Hexa Platform",
        "year": datetime.now().year
    }
)

# Enviar email con template
await email_service.send_template_email(command)
```

### 3. Envío en Batch

```python
from modules.email.application.dto import SendEmailCommand

commands = [
    SendEmailCommand(
        to=["user1@example.com"],
        subject="Notificación",
        body="Contenido del mensaje 1"
    ),
    SendEmailCommand(
        to=["user2@example.com"],
        subject="Notificación",
        body="Contenido del mensaje 2"
    )
]

# Enviar múltiples emails
result = await email_service.send_bulk_email(commands)
print(f"Enviados: {result['success']}, Fallidos: {result['failed']}")
```

### 4. Uso desde otros módulos (Service Locator)

```python
from shared.interfaces.service_locator import service_locator
from modules.email.application.dto import SendTemplateEmailCommand

# Obtener servicio de email
email_service = service_locator.get_service("email")

# Usar el servicio
command = SendTemplateEmailCommand(
    to=["usuario@example.com"],
    subject="Reset de Contraseña",
    template_name="password_reset.html",
    template_data={
        "user_name": "Juan Pérez",
        "reset_code": "ABC123",
        "expiration_time": 15,
        "app_name": "Hexa Platform",
        "year": 2025
    }
)

await email_service.send_template_email(command)
```

## Templates Disponibles

### 1. welcome.html
Template para emails de bienvenida.

**Variables:**
- `user_name`: Nombre del usuario
- `user_email`: Email del usuario
- `company_name`: Nombre de la empresa (opcional)
- `activation_link`: Link de activación (opcional)
- `app_name`: Nombre de la aplicación
- `year`: Año actual

### 2. password_reset.html
Template para reset de contraseña.

**Variables:**
- `user_name`: Nombre del usuario
- `reset_code`: Código de verificación (opcional)
- `reset_link`: Link para reset (opcional)
- `expiration_time`: Tiempo de expiración en minutos
- `app_name`: Nombre de la aplicación
- `year`: Año actual

### 3. notification.html
Template genérico para notificaciones.

**Variables:**
- `user_name`: Nombre del usuario
- `notification_title`: Título de la notificación
- `message_title`: Título del mensaje
- `message_body`: Cuerpo del mensaje
- `details`: Dict con detalles adicionales (opcional)
- `action_link`: Link de acción (opcional)
- `action_text`: Texto del botón (opcional)
- `app_name`: Nombre de la aplicación
- `year`: Año actual

## Crear Templates Personalizados

1. Crear un archivo HTML en `backend/modules/email/templates/`
2. Usar sintaxis Jinja2 para variables dinámicas:

```html
<!DOCTYPE html>
<html>
<body>
    <h1>Hola {{ user_name }}</h1>
    <p>{{ message }}</p>

    {% if show_button %}
    <a href="{{ button_link }}">{{ button_text }}</a>
    {% endif %}
</body>
</html>
```

3. Usar el template:

```python
command = SendTemplateEmailCommand(
    to=["user@example.com"],
    subject="Mi Template",
    template_name="mi_template.html",
    template_data={
        "user_name": "Juan",
        "message": "Este es un mensaje personalizado",
        "show_button": True,
        "button_link": "https://example.com",
        "button_text": "Haz clic aquí"
    }
)
```

## Manejo de Errores

```python
from modules.email.domain.exception import (
    EmailSendException,
    TemplateNotFoundException,
    TemplateRenderException
)

try:
    await email_service.send_template_email(command)
except TemplateNotFoundException as e:
    print(f"Template no encontrado: {e.message}")
except TemplateRenderException as e:
    print(f"Error al renderizar template: {e.message}")
except EmailSendException as e:
    print(f"Error al enviar email: {e.message}")
```

## Testing

```python
# tests/test_email_service.py
import pytest
from modules.email.application.dto import SendEmailCommand

@pytest.mark.asyncio
async def test_send_email(email_service):
    command = SendEmailCommand(
        to=["test@example.com"],
        subject="Test",
        body="Test message"
    )

    result = await email_service.send_email(command)
    assert result == True
```

## Integración con el Sistema

El módulo Email sigue la arquitectura hexagonal del proyecto y se integra mediante:

1. **Dependency Injection**: Container definido en `container.py`
2. **Service Protocol**: Interface definida en `shared/interfaces/service_protocols.py`
3. **Service Locator**: Disponible globalmente como `service_locator.get_service("email")`

## Seguridad

- ✅ Conexión SSL/TLS para comunicación segura
- ✅ Autenticación SMTP
- ✅ Validación de entidades Email
- ✅ Sanitización automática de HTML en templates (Jinja2 autoescape)

## Notas

- El puerto 587 usa STARTTLS, el puerto 465 usa SSL directo
- Para Gmail, puede ser necesario usar "App Passwords" en lugar de la contraseña normal
- Los templates usan autoescape por defecto para prevenir XSS
