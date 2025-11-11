from core.fastapi.dependencies.permission import PermissionGroup


class RolePermission(PermissionGroup):
	group = "role"

	read = "Lee roles"
	write = "Crea roles"
	delete = "Elimina roles"


class GroupPermission(PermissionGroup):
	group = "group"

	read = "Lee grupos de permisos"
	write = "Crea grupos de permisos"
	delete = "Elimina grupos de permisos"


class PermissionPermission(PermissionGroup):
	group = "permission"

	read = "Lee permisos"
	write = "Crea permisos"
	delete = "Elimina permisos"
