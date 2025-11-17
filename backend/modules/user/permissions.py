from core.fastapi.dependencies.permission import PermissionGroup


class UserPermission(PermissionGroup):
	group = "user"

	read = "Lee usuarios"
	write = "Crea usuarios"
	delete = "Elimina usuarios"
