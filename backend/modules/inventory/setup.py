"""
Inventory Module Setup
Módulo de gestión de inventario y productos
"""
from core.config.modules import ModuleSetup


class InventoryModule(ModuleSetup):
    """
    Módulo de Inventario

    Permite gestionar el inventario de productos, incluyendo:
    - Registro de productos
    - Control de stock
    - Movimientos de inventario
    - Alertas de stock bajo
    """
    name = "Inventory"
    token = "inventory"
    description = "Gestión de inventario y control de stock de productos"
