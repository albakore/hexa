from modules.yiqi_erp.domain.entity.factura_compra import FacturaDeCompra
import rich as r

factura = FacturaDeCompra()

print(factura.model_dump(by_alias=True, include={"CUCO_ID_CUGA": True}))
print(factura.get_attributes())
