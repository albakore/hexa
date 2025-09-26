#!/usr/bin/env python3
"""
Versión mínima de la aplicación que funciona sin dependencias complejas
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Dependency injection is handled by core.fastapi.server

# Import all module routers
from modules.finance.adapter.input.api.v1.currency import currency_router
from modules.app_module.adapter.input.api.v1.module import module_router
from modules.user_relationships.adapter.input.api.v1.user_relationship import user_relationship_router
from modules.yiqi_erp.adapter.input.api.v1.yiqi_erp import yiqi_erp_router
from modules.rbac.adapter.input.api.v1.rbac import rbac_router
from modules.auth.adapter.input.api.v1.auth import auth_router
from modules.provider.adapter.input.api.v1.provider import provider_router
from modules.provider.adapter.input.api.v1.draft_invoice import draft_invoice_router
from modules.user.adapter.input.api.v1.user import user_router

# Container initialization is handled by core.fastapi.server

# Crear aplicación mínima
app = FastAPI(
	title="Fast Hexagonal API",
	description="API completa con todos los módulos",
	version="2.0.0",
)

# Configurar CORS
app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)


@app.get("/")
async def root():
	return {
		"message": "Fast Hexagonal API - Minimal Version",
		"status": "running",
		"version": "2.0.0-minimal",
	}


@app.get("/health")
async def health_check():
	return {
		"status": "healthy",
		"message": "Minimal version running successfully",
		"architecture": "hexagonal_decoupled_minimal",
	}


@app.get("/modules")
async def list_modules():
	return {
		"message": "All modules active and loaded",
		"active_modules": [
			"auth",
			"users", 
			"rbac",
			"finance",
			"providers",
			"user-relationships",
			"yiqi-erp",
			"modules"
		],
		"total_routes": 9
	}


# Include all module routers
app.include_router(auth_router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(user_router, prefix="/api/v1/users", tags=["Users"])
app.include_router(rbac_router, prefix="/api/v1/rbac", tags=["RBAC"])
app.include_router(currency_router, prefix="/api/v1/finance/currencies", tags=["Finance"])
app.include_router(provider_router, prefix="/api/v1/providers", tags=["Providers"])
app.include_router(draft_invoice_router, prefix="/api/v1/providers/draft-invoices", tags=["Provider Invoices"])
app.include_router(user_relationship_router, prefix="/api/v1/user-relationships", tags=["User Relationships"])
app.include_router(yiqi_erp_router, prefix="/api/v1/yiqi-erp", tags=["YiQi ERP"])
app.include_router(module_router, prefix="/api/v1/modules", tags=["Modules"])


if __name__ == "__main__":
	import uvicorn

	uvicorn.run(app, host="0.0.0.0", port=8000)
