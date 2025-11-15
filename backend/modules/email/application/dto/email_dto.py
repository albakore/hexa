from dataclasses import dataclass
from typing import Optional, List, Dict, Any


@dataclass
class SendEmailCommand:
    """
    Comando para enviar un email simple.

    Attributes:
        to: Lista de destinatarios
        subject: Asunto del email
        body: Cuerpo del email (HTML o texto plano)
        from_email: Email del remitente (opcional)
        cc: Destinatarios en copia (opcional)
        bcc: Destinatarios en copia oculta (opcional)
        is_html: Si el cuerpo es HTML (default: True)
    """
    to: List[str]
    subject: str
    body: str
    from_email: Optional[str] = None
    cc: Optional[List[str]] = None
    bcc: Optional[List[str]] = None
    is_html: bool = True


@dataclass
class SendTemplateEmailCommand:
    """
    Comando para enviar un email usando un template.

    Attributes:
        to: Lista de destinatarios
        subject: Asunto del email
        template_name: Nombre del archivo template (ej: "welcome.html")
        template_data: Datos dinámicos para renderizar en el template
        from_email: Email del remitente (opcional)
        cc: Destinatarios en copia (opcional)
        bcc: Destinatarios en copia oculta (opcional)
    """
    to: List[str]
    subject: str
    template_name: str
    template_data: Dict[str, Any]
    from_email: Optional[str] = None
    cc: Optional[List[str]] = None
    bcc: Optional[List[str]] = None
