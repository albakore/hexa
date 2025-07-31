
from dependency_injector.wiring import Provide
from fastapi import APIRouter, Depends
from modules.container import ModuleContainer


draft_invoice_router = APIRouter()

# @draft_invoice_router.get("")
# @inject
# async def get_all_draft_invoices(
# 	limit: int = Query(default=10, ge=1, le=50),
# 	page: int = Query(default=0),
# 	service : ProviderService = Depends(Provide[ModuleContainer.provider.service])
# ):
# 	return await service.get_all_draft_invoices(limit,page)
