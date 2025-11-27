"""
Módulo de Finance
Configuración simplificada usando variables y funciones
"""

from typing import Dict

from fastapi import APIRouter

from modules.finance.container import FinanceContainer


def setup_routes() -> APIRouter:
	"""Configura las rutas del módulo"""
	from .adapter.input.api.v1.currency import currency_router as currency_v1_router

	router = APIRouter(prefix="/finance", tags=["Finance"])
	router.include_router(currency_v1_router, prefix="/v1/currency", tags=["Finance"])

	return router


# Configuración del módulo
name = "finance"
container = FinanceContainer()
service: Dict[str, object] = {
	"currency_service": container.currency_service,
}
routes = setup_routes()
