"""
Ejemplos de uso del módulo Email

Este archivo contiene ejemplos de cómo usar el servicio de email
en diferentes escenarios.
"""

import asyncio
from datetime import datetime
from modules.email.application.dto import SendEmailCommand, SendTemplateEmailCommand
from modules.email.container import EmailContainer


async def example_simple_email():
    """Ejemplo de envío de email simple"""
    container = EmailContainer()
    email_service = container.service()

    command = SendEmailCommand(
        to=["usuario@example.com"],
        subject="Prueba de Email Simple",
        body="<h1>Hola!</h1><p>Este es un email de prueba.</p>",
        is_html=True
    )

    result = await email_service.send_email(command)
    print(f"Email enviado: {result}")


async def example_welcome_email():
    """Ejemplo de email de bienvenida con template"""
    container = EmailContainer()
    email_service = container.service()

    command = SendTemplateEmailCommand(
        to=["usuario@example.com"],
        subject="Bienvenido a Hexa Platform",
        template_name="welcome.html",
        template_data={
            "user_name": "Juan Pérez",
            "user_email": "usuario@example.com",
            "company_name": "Empresa ABC",
            "activation_link": "https://plataforma.com/activate/abc123",
            "app_name": "Hexa Platform",
            "year": datetime.now().year
        }
    )

    result = await email_service.send_template_email(command)
    print(f"Email de bienvenida enviado: {result}")


async def example_password_reset_email():
    """Ejemplo de email de reset de contraseña"""
    container = EmailContainer()
    email_service = container.service()

    command = SendTemplateEmailCommand(
        to=["usuario@example.com"],
        subject="Restablecer tu contraseña",
        template_name="password_reset.html",
        template_data={
            "user_name": "Juan Pérez",
            "reset_code": "ABC123",
            "reset_link": "https://plataforma.com/reset-password/token456",
            "expiration_time": 15,
            "app_name": "Hexa Platform",
            "year": datetime.now().year
        }
    )

    result = await email_service.send_template_email(command)
    print(f"Email de reset enviado: {result}")


async def example_notification_email():
    """Ejemplo de email de notificación genérica"""
    container = EmailContainer()
    email_service = container.service()

    command = SendTemplateEmailCommand(
        to=["usuario@example.com"],
        subject="Nueva factura procesada",
        template_name="notification.html",
        template_data={
            "user_name": "Juan Pérez",
            "notification_title": "Factura Procesada",
            "message_title": "Tu factura ha sido procesada exitosamente",
            "message_body": "La factura #12345 ha sido procesada y enviada al ERP.",
            "details": {
                "Número de Factura": "12345",
                "Fecha": "30/10/2025",
                "Monto": "$1,500.00",
                "Proveedor": "Proveedor XYZ"
            },
            "action_link": "https://plataforma.com/invoices/12345",
            "action_text": "Ver Factura",
            "app_name": "Hexa Platform",
            "year": datetime.now().year
        }
    )

    result = await email_service.send_template_email(command)
    print(f"Email de notificación enviado: {result}")


async def example_bulk_email():
    """Ejemplo de envío en batch"""
    container = EmailContainer()
    email_service = container.service()

    commands = [
        SendEmailCommand(
            to=["user1@example.com"],
            subject="Notificación Masiva",
            body="<p>Mensaje para usuario 1</p>",
            is_html=True
        ),
        SendEmailCommand(
            to=["user2@example.com"],
            subject="Notificación Masiva",
            body="<p>Mensaje para usuario 2</p>",
            is_html=True
        ),
        SendEmailCommand(
            to=["user3@example.com"],
            subject="Notificación Masiva",
            body="<p>Mensaje para usuario 3</p>",
            is_html=True
        )
    ]

    result = await email_service.send_bulk_email(commands)
    print(f"Resultados batch:")
    print(f"  Total: {result['total']}")
    print(f"  Exitosos: {result['success']}")
    print(f"  Fallidos: {result['failed']}")
    if result['errors']:
        print(f"  Errores: {result['errors']}")


async def example_email_with_cc_bcc():
    """Ejemplo de email con CC y BCC"""
    container = EmailContainer()
    email_service = container.service()

    command = SendEmailCommand(
        to=["destinatario@example.com"],
        cc=["copia@example.com"],
        bcc=["copia_oculta@example.com"],
        subject="Email con CC y BCC",
        body="<p>Este email tiene destinatarios en copia.</p>",
        is_html=True
    )

    result = await email_service.send_email(command)
    print(f"Email con CC/BCC enviado: {result}")


if __name__ == "__main__":
    # Descomentar el ejemplo que quieras ejecutar

    # asyncio.run(example_simple_email())
    # asyncio.run(example_welcome_email())
    # asyncio.run(example_password_reset_email())
    # asyncio.run(example_notification_email())
    # asyncio.run(example_bulk_email())
    # asyncio.run(example_email_with_cc_bcc())

    print("Descomenta el ejemplo que quieras ejecutar en el __main__")
