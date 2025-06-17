from fastapi import APIRouter


rbac_router = APIRouter()


@rbac_router.get("/role")
async def get_all_roles(): ...


@rbac_router.get("/role/{id_role}")
async def get_role(id_role: int): ...


@rbac_router.post("/role")
async def create_role(): ...


@rbac_router.put("/role")
async def edit_role(): ...


@rbac_router.delete("/role/{id_role}")
async def delete_role(id_role: int): ...


@rbac_router.get("/permission")
async def get_all_permissions(): ...


@rbac_router.get("/permission/{id_permission}")
async def get_permission(id_permission: int): ...


@rbac_router.post("/permission")
async def create_permission(permission): ...


@rbac_router.put("/permission")
async def edit_permission(permission): ...


@rbac_router.delete("/permission/{id_permission}")
async def delete_permission(id_permission: int): ...
