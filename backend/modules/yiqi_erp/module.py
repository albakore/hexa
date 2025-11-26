"""
Módulo de Yiqi ERP
Configuración simplificada usando variables y funciones
"""

from typing import Dict

from fastapi import APIRouter

from modules.yiqi_erp.adapter.input.tasks.yiqi_erp import (
	create_invoice_from_purchase_invoice_tasks,
)
from modules.yiqi_erp.adapter.input.tasks.yiqi_erp_improved import (
	create_invoice_from_purchase_invoice_improved_tasks,
)
from modules.yiqi_erp.container import YiqiContainer


def setup_routes() -> APIRouter:
	"""Configura las rutas del módulo"""
	from .adapter.input.api.v1.yiqi_erp import yiqi_erp_router as yiqi_erp_v1_router

	router = APIRouter(prefix="/yiqi_erp", tags=["Yiqi ERP"])
	router.include_router(yiqi_erp_v1_router, prefix="/v1/yiqi_erp", tags=["Yiqi ERP"])

	return router


# Configuración del módulo
name = "yiqi_erp"
container = YiqiContainer()
service: Dict[str, object] = {
	"yiqi_service": container.service,
	"yiqi_erp_tasks": {
		"create_invoice_from_purchase_invoice_tasks": {
			"task": create_invoice_from_purchase_invoice_tasks,
			"config": {
				"autoretry_for": (Exception,),
				"retry_kwargs": {"max_retries": 5},
				"retry_backoff": True,
				"retry_backoff_max": 600,
				"retry_jitter": True,
			},
		},
		"create_invoice_from_purchase_invoice_improved_tasks": {
			"task": create_invoice_from_purchase_invoice_improved_tasks,
			"config": {
				"autoretry_for": (Exception,),
				"retry_kwargs": {"max_retries": 5},
				"retry_backoff": True,
				"retry_backoff_max": 600,
				"retry_jitter": True,
			},
		},
	},
}
routes = setup_routes()
