from sqlmodel import SQLModel, Field


class AirWaybill(SQLModel, table=True):
	id: int | None = Field(None, primary_key=True)
	fk_provider: int | None = Field(default=None, description="ID del proveedor")
	fk_draft_invoice: int | None = Field(
		default=None, description="ID de la factura de compra draft"
	)
	fk_purchase_invoice: int | None = Field(
		default=None, description="ID de la factura de compra"
	)
	awb_code: str | None = Field(default=None, description="Código de la guía aérea")
	origin: str | None = Field(default=None, description="Origen de la guía aérea")
	destination: str | None = Field(
		default=None, description="Destino de la guía aérea"
	)
	kg: float | None = Field(default=None, description="Peso en kg")
	fk_yiqi_awb: int | None = Field(
		default=None, description="ID de la guía aérea en YiqiERP"
	)
