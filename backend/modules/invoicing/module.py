"""
Módulo de Invoicing
Configuración simplificada usando variables y funciones
"""

from typing import Dict

from fastapi import APIRouter

from modules.invoicing.container import InvoicingContainer


def setup_routes() -> APIRouter:
	"""Configura las rutas del módulo"""
	from .adapter.input.api.v1.purchase_invoice import (
		purchase_invoice_router as purchase_invoice_v1_router,
	)

	router = APIRouter(prefix="/invoicing", tags=["Invoicing"])
	router.include_router(purchase_invoice_v1_router, prefix="/v1/purchase_invoice")

	return router


# Configuración del módulo
name = "invoicing"
container = InvoicingContainer()
service: Dict[str, object] = {
	"purchase_invoice_service": container.purchase_invoice_service,
}
routes = setup_routes()
