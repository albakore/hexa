from dataclasses import dataclass
from typing import Optional, List, Dict, Any


@dataclass
class EmailAttachment:
    """Representa un archivo adjunto en un email"""
    filename: str
    content: bytes
    content_type: str = "application/octet-stream"


@dataclass
class Email:
    """
    Entidad de dominio que representa un email.

    Attributes:
        to: Lista de destinatarios
        subject: Asunto del email
        body: Cuerpo del email (puede ser HTML o texto plano)
        from_email: Email del remitente (opcional, usa default del sistema)
        cc: Lista de destinatarios en copia (opcional)
        bcc: Lista de destinatarios en copia oculta (opcional)
        attachments: Lista de archivos adjuntos (opcional)
        is_html: Indica si el cuerpo es HTML (default: True)
        template_data: Datos dinámicos para renderizar en el template (opcional)
    """
    to: List[str]
    subject: str
    body: str
    from_email: Optional[str] = None
    cc: Optional[List[str]] = None
    bcc: Optional[List[str]] = None
    attachments: Optional[List[EmailAttachment]] = None
    is_html: bool = True
    template_data: Optional[Dict[str, Any]] = None

    def __post_init__(self):
        """Validaciones básicas"""
        if not self.to or len(self.to) == 0:
            raise ValueError("El email debe tener al menos un destinatario")
        if not self.subject:
            raise ValueError("El email debe tener un asunto")
        if not self.body:
            raise ValueError("El email debe tener un cuerpo")
