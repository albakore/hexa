from sqlmodel import Session, select
from typing import List
from uuid import UUID
from app.user_relationships.infra.output.registry import EntidadRelacionRegistry
from .models import UsuarioEntidadLink

class UserRelationshipService:
    def __init__(self, session: Session):
        self.session = session

    def obtener_entidades(self, usuario_id: UUID, tipo: str) -> List:
        modelo = EntidadRelacionRegistry.obtener_modelo(tipo)
        stmt = (
            select(modelo)
            .join(UsuarioEntidadLink, UsuarioEntidadLink.entidad_id == modelo.id)
            .where(
                (UsuarioEntidadLink.usuario_id == usuario_id)
                & (UsuarioEntidadLink.entidad_tipo == tipo)
            )
        )
        return self.session.exec(stmt).all()