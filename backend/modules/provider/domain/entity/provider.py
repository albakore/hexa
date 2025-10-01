from typing import TYPE_CHECKING, List
import uuid
from sqlmodel import SQLModel, Relationship, Field

from app.user_relationships.shared.decorators import user_relationship
from modules.provider.domain.entity.purchase_invoice_service import (
	ProviderInvoiceServiceLink,
)

if TYPE_CHECKING:
	from app.user.domain.entity.user import User
	from modules.provider.domain.entity.purchase_invoice_service import (
		PurchaseInvoiceService,
	)


class UserProviderLink(SQLModel, table=True):
	fk_user: uuid.UUID | None = Field(
		default=None, primary_key=True, foreign_key="user.id"
	)
	fk_provider: int | None = Field(
		default=None, primary_key=True, foreign_key="provider.id"
	)


@user_relationship("provider")
class Provider(SQLModel, table=True):
	id: int | None = Field(None, primary_key=True)
	name: str

	id_yiqi_provider: int | None = Field(None)

	users: List["User"] = Relationship(
		back_populates="providers", link_model=UserProviderLink
	)
	services: List["PurchaseInvoiceService"] = Relationship(
		back_populates="providers", link_model=ProviderInvoiceServiceLink
	)
