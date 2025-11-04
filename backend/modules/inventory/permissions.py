"""
Inventory Module Permissions
Define los permisos del módulo de inventario
"""
from core.fastapi.dependencies.permission import PermissionGroup


class ModuleInventoryPermission(PermissionGroup):
    """
    Permisos del módulo de inventario

    Genera los siguientes tokens de permiso:
    - inventory:read - Ver productos y stock
    - inventory:create - Crear nuevos productos
    - inventory:update - Modificar productos existentes
    - inventory:delete - Eliminar productos
    - inventory:stock_adjust - Ajustar niveles de stock
    - inventory:stock_movement - Ver movimientos de stock
    """
    group = "inventory"

    # Permisos básicos CRUD
    read = "Ver productos y consultar stock"
    create = "Crear nuevos productos en el inventario"
    update = "Modificar información de productos"
    delete = "Eliminar productos del inventario"

    # Permisos de gestión de stock
    stock_adjust = "Ajustar niveles de stock manualmente"
    stock_movement = "Ver historial de movimientos de stock"
    stock_transfer = "Transferir stock entre ubicaciones"

    # Permisos de reportes
    report_view = "Ver reportes de inventario"
    report_export = "Exportar reportes de inventario"
