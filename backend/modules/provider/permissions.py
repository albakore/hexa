from core.fastapi.dependencies.permission import (
	PermissionGroup
)

class ModuleProviderPermission(PermissionGroup):
    group = "providers"

    read = "Lee proveedores"
    write = "Crea proveedores"
    update = "Modifica proveedores"
    delete = "Elimina proveedores"
    invoices_read = "Visualiza las facturas del proveedor"
    invoices_write = "Crea facturas del proveedor"
    invoices_update = "Modifica facturas del proveedor"
    invoices_delete = "Borra facturas del proveedor"
    invoices_push_yiqi = "Envia facturas del proveedor a yiqi"