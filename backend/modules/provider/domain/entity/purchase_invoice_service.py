from datetime import date, datetime
from typing import TYPE_CHECKING, List
import uuid
from sqlmodel import SQLModel, Relationship, Field, PrimaryKeyConstraint

if TYPE_CHECKING:
	from modules.provider.domain.entity.provider import Provider


class ProviderInvoiceServiceLink(SQLModel, table=True):
	fk_provider: int | None = Field(primary_key=True, foreign_key="provider.id")
	fk_service: int | None = Field(
		primary_key=True, foreign_key="purchaseinvoiceservice.id"
	)


class PurchaseInvoiceService(SQLModel, table=True):
	id: int | None = Field(None, primary_key=True)
	name: str = Field(default=None, description="Nombre del servicio")
	description: str | None = Field(
		default=None, description="Descripcion del servicio"
	)
	group: str | None = Field(
		default=None, description="Grupo al que pertenece este servicio"
	)

	require_awb: bool | None = Field(default=None)
	require_unit_price: bool | None = Field(default=None)
	require_kg: bool | None = Field(default=None)
	require_items: bool | None = Field(default=None)
	require_detail_file: bool | None = Field(default=None)

	providers: List["Provider"] = Relationship(
		back_populates="services", link_model=ProviderInvoiceServiceLink
	)

	id_yiqi_service: int | None = Field(
		default=None, description="Id service from Yiqi"
	)
