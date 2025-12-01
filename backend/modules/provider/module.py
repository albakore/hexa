"""
Módulo de Provider
Configuración simplificada usando variables y funciones
"""

from typing import Dict

from fastapi import APIRouter

from modules.provider.container import ProviderContainer


def setup_routes() -> APIRouter:
	"""Configura las rutas del módulo"""
	from .adapter.input.api.v1.draft_invoice import (
		draft_invoice_router as draft_invoice_v1_router,
	)
	from .adapter.input.api.v1.provider import provider_router as provider_v1_router
	from .adapter.input.api.v1.purchase_invoice_service import (
		purchase_invoice_service_router as purchase_invoice_service_v1_router,
	)
	from .adapter.input.api.v1.air_waybill import (
	air_waybill_router as air_waybill_v1_router,
	)


	router = APIRouter(prefix="/providers", tags=["Providers"])
	router.include_router(
		provider_v1_router, prefix="/v1/providers", tags=["Providers"]
	)
	router.include_router(
		draft_invoice_v1_router,
		prefix="/v1/draft_invoice",
		tags=["Providers Draft Invoice"],
	)
	router.include_router(
		purchase_invoice_service_v1_router,
		prefix="/v1/purchase_invoice_service",
		tags=["Providers Draft Invoice[Service]"],
	)
	router.include_router(
		air_waybill_v1_router,
		prefix="/v1/air_waybill",
		tags=["Providers Air Waybill"],
	)

	return router


# Configuración del módulo
name = "provider"
container = ProviderContainer()
service: Dict[str, object] = {
	"provider_service": container.provider_service,
	"draft_invoice_service": container.draft_invoice_service,
	"draft_invoice_servicetype_service": container.invoice_servicetype_service,
	"air_waybill_service": container.air_waybill_service,	
}
routes = setup_routes()
